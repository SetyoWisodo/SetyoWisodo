"""Konektor data NYATA untuk memantau dompet whale di Solana.

Modul ini **tidak** menandatangani transaksi dan tidak menyimpan private key.
Ia hanya membaca aktivitas publik sebuah dompet dan mengubahnya menjadi objek
``WhaleTx`` yang formatnya sama dengan yang dipakai simulator.

Butuh internet + API key (gratis sampai kuota tertentu):

    export HELIUS_API_KEY=xxxxxxxx

    python run.py whale-watch --wallets wallets.json

Catatan jujur soal keterbatasan data publik:

* Endpoint "enhanced transactions" Helius memberi tahu SPL token apa yang
  dibeli sebuah dompet, berapa banyak, dan kapan.
* Yang **tidak** tersedia gratis: porsi supply dev, bundle %, status LP lock,
  riwayat rug per dev. Untuk forensics kelas produksi kamu butuh indexer
  berbayar (Helius DAS, Birdeye, Solscan Pro) atau mem-parse sendiri akun
  token & pool on-chain.
* Karena itu FILTER di repo ini menolak saat data tidak diketahui — dan itu
  perilaku yang benar. Jangan pernah mengganti "tidak tahu" dengan "anggap aman".

Di sandbox Arena modul ini akan gagal terhubung (egress dibatasi ke GitHub/PyPI).
Jalankan di mesinmu sendiri.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .whale_market import WhaleTx

HELIUS_BASE = "https://api.helius.xyz/v0/addresses/{wallet}/transactions"
DEXSCREENER = "https://api.dexscreener.com/latest/dex/tokens/{mint}"


@dataclass
class WatchedWallet:
    address: str
    label: str = "whale"
    min_usd: float = 2_000.0


def load_wallets(path: str | Path) -> list[WatchedWallet]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for row in data:
        if isinstance(row, str):
            out.append(WatchedWallet(address=row))
        else:
            out.append(WatchedWallet(
                address=row["address"], label=row.get("label", "whale"),
                min_usd=float(row.get("min_usd", 2_000)),
            ))
    return out


class HeliusWhaleMonitor:
    """Polling aktivitas dompet. Ringan, tanpa websocket, aman untuk diuji."""

    def __init__(self, wallets: list[WatchedWallet], api_key: str,
                 poll_seconds: float = 6.0, limit: int = 20):
        self.wallets = wallets
        self.api_key = api_key
        self.poll_seconds = poll_seconds
        self.limit = limit
        self.tick = 0
        self.seen: set[str] = set()
        self.pending: list[WhaleTx] = []
        self.errors: list[str] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ HTTP
    def _get(self, url: str, timeout: float = 10.0):
        req = urllib.request.Request(url, headers={"User-Agent": "pumpkin-terminal/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())

    def fetch(self, wallet: WatchedWallet) -> list[WhaleTx]:
        url = HELIUS_BASE.format(wallet=wallet.address)
        url += f"?api-key={self.api_key}&limit={self.limit}"
        try:
            rows = self._get(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            self.errors.append(f"{wallet.address[:8]}: {exc}")
            self.errors = self.errors[-5:]
            return []
        if not isinstance(rows, list):
            return []

        out: list[WhaleTx] = []
        for tx in rows:
            sig = str(tx.get("signature", ""))
            if not sig or sig in self.seen:
                continue
            self.seen.add(sig)
            ts = int(tx.get("timestamp") or 0)
            for tr in tx.get("tokenTransfers") or []:
                mint = str(tr.get("mint", ""))
                if not mint or mint == "So11111111111111111111111111111111111111112":
                    continue
                amount = _to_float(tr.get("tokenAmount"))
                # arah: whale menerima token = buy, mengirim = sell
                direction = "buy" if tr.get("toUserAccount") == wallet.address else "sell"
                price = self._price_usd(mint)
                usd = amount * price if price else 0.0
                if usd < wallet.min_usd and direction == "buy":
                    continue
                out.append(WhaleTx(
                    tick=ts, whale=wallet.address, label=wallet.label, token=mint,
                    symbol=(tr.get("symbol") or mint[:4]).upper(),
                    side=direction, usd=usd, price=price or 0.0,
                ))
        return out

    def _price_usd(self, mint: str) -> float:
        try:
            data = self._get(DEXSCREENER.format(mint=mint), timeout=6.0)
            pairs = data.get("pairs") or []
            if pairs:
                return float(pairs[0].get("priceUsd") or 0.0)
        except Exception:
            return 0.0
        return 0.0

    # ------------------------------------------------------------------ loop
    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            for w in self.wallets:
                for tx in self.fetch(w):
                    with self._lock:
                        self.pending.append(tx)
                time.sleep(1.0)   # sopan ke rate limit
            self._stop.wait(self.poll_seconds)

    def drain(self) -> list[WhaleTx]:
        with self._lock:
            out, self.pending = self.pending, []
        return out

    def stop(self) -> None:
        self._stop.set()


def _to_float(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0
