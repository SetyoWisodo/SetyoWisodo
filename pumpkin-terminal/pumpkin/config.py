"""Konfigurasi Pumpkin Terminal.

Semua aturan agen dikumpulkan di sini supaya bisa diubah tanpa menyentuh logika.
Nilai default sengaja dibuat konservatif (mirip desk memecoin yang wajar).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Literal

ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "runs"


@dataclass
class FilterRules:
    """Aturan keras FILTER. Gagal satu aturan = token langsung dibuang."""

    min_liquidity_usd: float = 16_000.0
    min_holders: int = 200
    max_top10_pct: float = 32.0
    max_dev_pct: float = 8.0
    require_mint_revoked: bool = True
    require_lp_locked: bool = True
    min_age_ticks: int = 4
    max_single_holder_pct: float = 6.0


@dataclass
class RiskRules:
    """Aturan SNIPER (ukuran posisi) + GUARD (exit)."""

    max_position_pct: float = 0.08        # maksimal 8% saldo per posisi
    max_concurrent: int = 3
    min_ticks_between_entries: int = 2
    max_pct_of_liquidity: float = 0.005   # posisi tidak boleh > 0.5% pool
    stop_loss_pct: float = 0.06           # stop-loss keras -6%
    trail_after_pct: float = 0.12         # trailing baru aktif setelah +12%
    trail_distance_pct: float = 0.08      # jarak trailing 8% dari puncak
    max_hold_ticks: int = 240             # paksa keluar kalau terlalu lama
    entry_fee_pct: float = 0.010          # fee DEX/platform
    exit_fee_pct: float = 0.010
    entry_slippage_pct: float = 0.015
    exit_slippage_pct: float = 0.020
    min_score: float = 0.60               # ANALYST: di bawah ini tidak ditembak

    @property
    def round_trip_cost_pct(self) -> float:
        return (
            self.entry_fee_pct
            + self.exit_fee_pct
            + self.entry_slippage_pct
            + self.exit_slippage_pct
        )


@dataclass
class SimConfig:
    """Parameter sesi simulasi (satu sesi = satu 'overnight session' versi cepat)."""

    start_balance: float = 80.0
    ticks: int = 1_800                  # total tick satu sesi
    tick_seconds_wall: float = 0.1      # 1 tick = 100 ms waktu nyata
    sim_seconds_per_tick: int = 5        # 1 tick = 5 detik waktu "pasar"
    tokens_per_tick: int = 7             # laju token baru (≈12.600 pair / sesi)
    seed: int = 7
    edge_mode: Literal["correlated", "null"] = "correlated"
    speed: float = 1.0                   # pengali kecepatan tick
    feed: Literal["sim", "dexscreener"] = "sim"

    @property
    def sim_minutes(self) -> float:
        return self.ticks * self.sim_seconds_per_tick / 60.0


@dataclass
class Config:
    sim: SimConfig = field(default_factory=SimConfig)
    filters: FilterRules = field(default_factory=FilterRules)
    risk: RiskRules = field(default_factory=RiskRules)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["risk"]["round_trip_cost_pct"] = self.risk.round_trip_cost_pct
        d["sim"]["sim_minutes"] = self.sim.sim_minutes
        return d


DEFAULT_CONFIG = Config()
