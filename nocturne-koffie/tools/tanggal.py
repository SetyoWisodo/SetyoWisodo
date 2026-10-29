"""Tanggal hari ini menurut zona waktu pemilik (Asia/Jakarta), bukan zona server."""
from __future__ import annotations

from datetime import date, datetime


def hari_ini() -> date:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Asia/Jakarta")).date()
    except Exception:
        return date.today()
