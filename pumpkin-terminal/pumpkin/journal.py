"""Jurnal trade persisten (SQLite, stdlib).

Gunanya bukan sekadar mencatat: setiap baris menyimpan **fitur yang dipakai saat
mengambil keputusan** dan **hasilnya**. Dengan begitu model bisa dilatih ulang
dari kenyataan (`AlphaEngine.fit_from_journal`), bukan dari tebakan.

Ini juga yang membuat klaim "win rate >70%" bisa diaudit: hitung sendiri dari
tabel `trades`, jangan percaya dashboard.
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT, tick INTEGER, ts REAL,
    token TEXT, symbol TEXT,
    p_win REAL, ev_pct REAL, tp REAL, sl REAL, size_pct REAL,
    features TEXT,
    entry_price REAL, exit_price REAL,
    pnl_pct REAL, pnl_usd REAL,
    reason TEXT, hold_ticks INTEGER,
    won INTEGER
);
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT, tick INTEGER, ts REAL,
    token TEXT, symbol TEXT, approved INTEGER,
    p_win REAL, coordination REAL, social REAL, safety REAL,
    reasons TEXT
);
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT, tick INTEGER, kind TEXT, direction INTEGER, headline TEXT
);
"""


class Journal:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def record_trade(self, *, session: str, tick: int, token: str, symbol: str,
                     p_win: float, ev_pct: float, tp: float, sl: float, size_pct: float,
                     features: dict, entry_price: float, exit_price: float,
                     pnl_pct: float, pnl_usd: float, reason: str, hold_ticks: int) -> None:
        self.conn.execute(
            "INSERT INTO trades (session,tick,ts,token,symbol,p_win,ev_pct,tp,sl,size_pct,"
            "features,entry_price,exit_price,pnl_pct,pnl_usd,reason,hold_ticks,won) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (session, tick, time.time(), token, symbol, p_win, ev_pct, tp, sl, size_pct,
             json.dumps(features), entry_price, exit_price, pnl_pct, pnl_usd, reason,
             hold_ticks, 1 if pnl_usd > 0 else 0))
        self.conn.commit()

    def record_decision(self, *, session: str, tick: int, token: str, symbol: str,
                        approved: bool, p_win: float, coordination: float,
                        social: float, safety: float, reasons: list[str]) -> None:
        self.conn.execute(
            "INSERT INTO decisions (session,tick,ts,token,symbol,approved,p_win,"
            "coordination,social,safety,reasons) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (session, tick, time.time(), token, symbol, 1 if approved else 0, p_win,
             coordination, social, safety, json.dumps(reasons)))
        self.conn.commit()

    def record_news(self, *, session: str, tick: int, kind: str, direction: int,
                    headline: str) -> None:
        self.conn.execute(
            "INSERT INTO news (session,tick,kind,direction,headline) VALUES (?,?,?,?,?)",
            (session, tick, kind, direction, headline))
        self.conn.commit()

    # ------------------------------------------------------------- pembacaan
    def rows(self, limit: int = 5_000) -> list[dict]:
        cur = self.conn.execute(
            "SELECT features, won FROM trades ORDER BY id DESC LIMIT ?", (limit,))
        out = []
        for features, won in cur.fetchall():
            try:
                f = json.loads(features)
            except (TypeError, ValueError):
                continue
            out.append({"features": f, "won": bool(won)})
        return out

    def summary(self) -> dict:
        cur = self.conn.execute(
            "SELECT COUNT(*), SUM(won), AVG(pnl_pct), SUM(pnl_usd) FROM trades")
        n, wins, avg_pct, total = cur.fetchone()
        n = n or 0
        wins = wins or 0
        return {
            "trades": n,
            "wins": wins,
            "win_rate": round(wins / n * 100, 2) if n else 0.0,
            "avg_pnl_pct": round((avg_pct or 0) * 100, 3),
            "total_pnl_usd": round(total or 0, 2),
        }

    def close(self) -> None:
        self.conn.close()
