"""
Vectorized quantitative indicator algorithms: VWAP, RVOL, ATR, and Consolidation Breakout detection.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from src.models.scanner_models import BreakoutType


def compute_vwap(prices: np.ndarray, volumes: np.ndarray) -> Tuple[float, float]:
    """
    Computes Volume Weighted Average Price (VWAP) and percentage deviation.
    VWAP = Sum(Typical Price * Volume) / Sum(Volume)
    """
    if len(prices) == 0 or len(volumes) == 0 or np.sum(volumes) == 0:
        return 0.0, 0.0

    typical_prices = prices  # or (H+L+C)/3
    cumulative_vp = np.sum(typical_prices * volumes)
    cumulative_vol = np.sum(volumes)

    vwap = float(cumulative_vp / cumulative_vol)
    last_price = float(prices[-1])
    deviation_pct = round(((last_price - vwap) / vwap) * 100, 2)

    return round(vwap, 2), deviation_pct


def compute_rvol(current_volume: float, baseline_20d_avg_volume: float) -> float:
    """
    Calculates Relative Volume (RVOL) multiple:
    RVOL = Current Volume / Baseline 20-Day Time-of-Day Average
    RVOL > 2.0 indicates institutional accumulation / momentum ignition.
    """
    if baseline_20d_avg_volume <= 0:
        return 1.0
    return round(current_volume / baseline_20d_avg_volume, 2)


def compute_atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> float:
    """
    Computes Wilder's Average True Range (ATR).
    """
    if len(closes) < 2:
        return float(highs[-1] - lows[-1]) if len(highs) > 0 else 1.0

    tr1 = highs[1:] - lows[1:]
    tr2 = np.abs(highs[1:] - closes[:-1])
    tr3 = np.abs(lows[1:] - closes[:-1])

    true_range = np.maximum(tr1, np.maximum(tr2, tr3))
    if len(true_range) < period:
        return round(float(np.mean(true_range)), 2)

    return round(float(np.mean(true_range[-period:])), 2)


def detect_consolidation_breakout(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    volumes: np.ndarray,
    lookback: int = 20,
    rvol_threshold: float = 2.0,
) -> Tuple[BreakoutType, str]:
    """
    Scans for Donchian Channel range squeeze and volume expansion breakout.
    """
    if len(closes) < lookback + 1:
        return BreakoutType.NONE, "Insufficient historical price bars."

    prev_highs = highs[-(lookback + 1):-1]
    prev_lows = lows[-(lookback + 1):-1]
    current_close = float(closes[-1])
    current_high = float(highs[-1])
    current_low = float(lows[-1])

    range_high = float(np.max(prev_highs))
    range_low = float(np.min(prev_lows))

    avg_volume = float(np.mean(volumes[-(lookback + 1):-1])) if len(volumes) > 1 else 1.0
    current_rvol = compute_rvol(float(volumes[-1]), avg_volume)

    # Bullish consolidation breakout
    if current_close > range_high:
        if current_rvol >= rvol_threshold:
            return BreakoutType.CONSOLIDATION_BREAKOUT_UP, f"Bullish breakout above {lookback}-bar high (${range_high:,.2f}) with high RVOL ({current_rvol}x)."
        return BreakoutType.CONSOLIDATION_BREAKOUT_UP, f"Bullish breakout above {lookback}-bar high (${range_high:,.2f}) with moderate volume ({current_rvol}x)."

    # Bearish consolidation breakdown
    if current_close < range_low:
        if current_rvol >= rvol_threshold:
            return BreakoutType.CONSOLIDATION_BREAKDOWN, f"Bearish breakdown below {lookback}-bar low (${range_low:,.2f}) with high volume ({current_rvol}x)."
        return BreakoutType.CONSOLIDATION_BREAKDOWN, f"Bearish breakdown below {lookback}-bar low (${range_low:,.2f})."

    # Volatility expansion without full range breach
    atr = compute_atr(highs, lows, closes, 14)
    current_bar_range = current_high - current_low
    if current_bar_range > (atr * 2.2) and current_rvol >= 1.8:
        return BreakoutType.VOLATILITY_EXPANSION, f"Abnormal volatility bar range (${current_bar_range:.2f} > 2.2x ATR) with RVOL {current_rvol}x."

    return BreakoutType.NONE, "Consolidating within historical price bands."


def calculate_momentum_score(
    rvol: float,
    change_24h_pct: float,
    vwap_deviation_pct: float,
    breakout_type: BreakoutType,
) -> float:
    """
    Computes composite quantitative momentum ranking score (0.0 to 100.0).
    Factors:
    - RVOL strength (up to 40 pts)
    - Price directional velocity (up to 30 pts)
    - VWAP alignment (up to 15 pts)
    - Breakout confirmation bonus (up to 15 pts)
    """
    # 1. RVOL Score (max 40)
    rvol_pts = min(40.0, max(0.0, (rvol / 4.0) * 40.0))

    # 2. Price Change Score (max 30)
    change_pts = min(30.0, max(0.0, abs(change_24h_pct) * 3.0))

    # 3. VWAP Alignment (max 15)
    vwap_pts = 15.0 if abs(vwap_deviation_pct) > 0.5 and (change_24h_pct * vwap_deviation_pct > 0) else 5.0

    # 4. Breakout Confirmation (max 15)
    breakout_pts = 15.0 if breakout_type != BreakoutType.NONE else 0.0

    total_score = round(rvol_pts + change_pts + vwap_pts + breakout_pts, 1)
    return min(100.0, max(0.0, total_score))
