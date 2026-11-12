"""
High-throughput scanning engine orchestrating multi-factor screening across universes.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import List, Optional
import numpy as np

from src.engine.indicators import (
    calculate_momentum_score,
    compute_atr,
    compute_vwap,
    detect_consolidation_breakout,
)
from src.models.scanner_models import (
    BreakoutType,
    ScanFilterCriteria,
    ScanResponse,
    ScannerResult,
    VWAPCondition,
)
from src.universes.market_universe import UniverseRegistry


class ScreenerEngine:
    """
    High-throughput screener evaluating relative volume, VWAP deviations, and breakouts.
    """

    def __init__(self):
        self.universe_registry = UniverseRegistry()

    def run_scan(self, criteria: ScanFilterCriteria) -> ScanResponse:
        start_time = time.perf_counter()
        instruments = self.universe_registry.get_instruments(
            asset_class=criteria.asset_class.value if criteria.asset_class else None
        )

        matches: List[ScannerResult] = []

        for sym, asset_cls, price, chg_pct, rvol, volume in instruments:
            # 1. Price Bounds Filter
            if price < criteria.min_price or price > criteria.max_price:
                continue

            # 2. Volume & RVOL Filters
            if volume < criteria.min_volume or rvol < criteria.min_rvol:
                continue

            # 3. Minimum Percentage Change Filter
            if criteria.min_change_pct is not None and chg_pct < criteria.min_change_pct:
                continue

            # Generate synthetic bar history to compute VWAP, ATR & Breakout status
            highs, lows, closes, vols = self.universe_registry.generate_synthetic_series(price, chg_pct)

            vwap_val, vwap_dev = compute_vwap(closes, vols)
            atr_val = compute_atr(highs, lows, closes, 14)
            breakout_type, signal_summary = detect_consolidation_breakout(
                highs, lows, closes, vols, lookback=20, rvol_threshold=criteria.min_rvol
            )

            # 4. VWAP Condition Filter
            if criteria.vwap_condition == VWAPCondition.ABOVE_VWAP and price < vwap_val:
                continue
            if criteria.vwap_condition == VWAPCondition.BELOW_VWAP and price > vwap_val:
                continue
            if criteria.vwap_condition == VWAPCondition.EXTREME_DEVIATION_UP and vwap_dev < 1.5:
                continue
            if criteria.vwap_condition == VWAPCondition.EXTREME_DEVIATION_DOWN and vwap_dev > -1.5:
                continue

            # Compute Momentum Composite Score
            score = calculate_momentum_score(rvol, chg_pct, vwap_dev, breakout_type)

            matches.append(
                ScannerResult(
                    symbol=sym,
                    asset_class=asset_cls,
                    current_price=round(price, 2) if price >= 1.0 else round(price, 4),
                    change_24h_pct=round(chg_pct, 2),
                    volume=volume,
                    rvol=rvol,
                    vwap=vwap_val,
                    vwap_deviation_pct=vwap_dev,
                    atr_14=atr_val,
                    breakout_type=breakout_type,
                    momentum_score=score,
                    signal_summary=signal_summary,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                )
            )

        # Rank descending by momentum composite score
        matches.sort(key=lambda x: x.momentum_score, reverse=True)
        final_results = matches[: criteria.max_results]

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return ScanResponse(
            scan_id=f"scan_{uuid.uuid4().hex[:8]}",
            total_screened=len(instruments),
            matching_count=len(final_results),
            execution_time_ms=elapsed_ms,
            results=final_results,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# Global singleton instance
screener_engine = ScreenerEngine()


def get_screener_engine() -> ScreenerEngine:
    return screener_engine
