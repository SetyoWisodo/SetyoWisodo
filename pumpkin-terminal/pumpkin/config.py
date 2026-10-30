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
class WhaleRules:
    """Aturan radar whale — inti 'big data' dari aliran dompet."""

    window_ticks: int = 6            # jendela agregasi sinyal
    min_whales_confirm: int = 3      # minimal whale berbeda sebelum dianggap sinyal
    min_net_inflow_usd: float = 8_000.0
    min_signal: float = 0.62
    max_rug_risk: float = 0.42       # forensics: tolak di atas ini
    max_chase_pct: float = 0.10      # jangan beli kalau harga sudah lari >12% dari sinyal
    min_whale_reputation: float = 0.35
    entry_delay_ticks: int = 1       # deteksi + forensics + inklusi transaksi
    max_tracked_tokens: int = 400


@dataclass
class ScalpRules:
    """Aturan eksekusi: 5% saldo per posisi, target +50% dalam hitungan detik."""

    position_pct: float = 0.05       # 5% dari total ekuitas
    take_profit_pct: float = 0.50
    stop_loss_pct: float = 0.08
    trail_after_pct: float = 0.18
    trail_distance_pct: float = 0.06
    max_hold_ticks: int = 12
    max_concurrent: int = 3
    max_pct_of_liquidity: float = 0.01
    entry_fee_pct: float = 0.010
    exit_fee_pct: float = 0.010
    entry_slippage_pct: float = 0.020
    exit_slippage_pct: float = 0.025

    @property
    def round_trip_cost_pct(self) -> float:
        return (self.entry_fee_pct + self.exit_fee_pct
                + self.entry_slippage_pct + self.exit_slippage_pct)

    @property
    def breakeven_hit_rate(self) -> float:
        """Hit-rate minimum agar target +50% / stop -20% tidak merugi.

        Menang = +50% - biaya, kalah = -20% - biaya.
        """
        win = self.take_profit_pct - self.round_trip_cost_pct
        loss = self.stop_loss_pct + self.round_trip_cost_pct
        return loss / (win + loss)


@dataclass
class WhaleSimConfig:
    start_balance: float = 250.0
    ticks: int = 2_400
    tick_seconds_wall: float = 0.1
    sim_seconds_per_tick: int = 2      # 1 tick ≈ 2 detik pasar (pump.fun cepat)
    tokens_per_tick: int = 6
    whales: int = 48
    seed: int = 21
    edge_mode: Literal["informed", "noise"] = "informed"
    speed: float = 1.0

    @property
    def sim_minutes(self) -> float:
        return self.ticks * self.sim_seconds_per_tick / 60.0


@dataclass
class SocialRules:
    """Aturan desk sosial: probabilitas, biaya, dan disiplin."""

    min_p_win: float = 0.72
    max_coordination: float = 0.50
    min_signal: float = 0.52
    entry_delay_ticks: int = 1
    cost_round_trip: float = 0.040
    stop_loss: float = 0.06
    min_tp: float = 0.08
    max_tp: float = 0.30
    tp1_fraction: float = 0.5          # ambil separuh posisi di 60% target
    max_hold_ticks: int = 15
    max_concurrent: int = 4
    max_position_pct: float = 0.05
    max_pct_of_liquidity: float = 0.01
    daily_loss_limit_pct: float = 0.02
    daily_target_pct: float = 0.01
    day_length_ticks: int = 900
    use_coordination_filter: bool = True
    use_forensics: bool = True
    use_committee: bool = False       # veto agregat komite — TERUKUR TIDAK MEMBANTU, default mati
    use_forecast_gate: bool = False   # diuji: netral (win rate +0.9pp, median -0.1pp) — opt-in
    bear_veto: float = 0.62           # skor keberatan yang langsung menolak
    bear_downsize_at: float = 0.50    # skor keberatan yang memperkecil posisi
    max_heat_pct: float = 0.08        # total risiko terbuka maksimum (ekuitas)
    withdraw_at_multiple: float = 2.0   # tarik modal saat ekuitas 2x modal awal


@dataclass
class SocialSimConfig:
    start_balance: float = 250.0
    ticks: int = 2400
    tick_seconds_wall: float = 0.08
    sim_seconds_per_tick: int = 3
    tokens_per_tick: int = 6
    whales: int = 48
    kols: int = 45
    bots: int = 220
    seed: int = 21
    mode: Literal["clean", "dirty"] = "dirty"   # dirty = ada bot farm
    speed: float = 1.0

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

    whale_sim: WhaleSimConfig = field(default_factory=WhaleSimConfig)
    whale: WhaleRules = field(default_factory=WhaleRules)
    scalp: ScalpRules = field(default_factory=ScalpRules)
    social: SocialRules = field(default_factory=SocialRules)
    social_sim: SocialSimConfig = field(default_factory=SocialSimConfig)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["risk"]["round_trip_cost_pct"] = self.risk.round_trip_cost_pct
        d["sim"]["sim_minutes"] = self.sim.sim_minutes
        d["scalp"]["round_trip_cost_pct"] = self.scalp.round_trip_cost_pct
        d["scalp"]["breakeven_hit_rate"] = self.scalp.breakeven_hit_rate
        d["whale_sim"]["sim_minutes"] = self.whale_sim.sim_minutes
        d["social_sim"]["sim_minutes"] = self.social_sim.sim_minutes
        return d



DEFAULT_CONFIG = Config()
