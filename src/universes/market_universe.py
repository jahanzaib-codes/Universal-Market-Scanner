"""
Multi-asset instrument universe definitions and live market tick simulation.
"""

from typing import Dict, List, Tuple
import numpy as np
from src.models.scanner_models import AssetClass


DEFAULT_UNIVERSE = [
    # US Equities (Mega Cap, Tech, High Beta)
    ("NVDA", AssetClass.EQUITY, 142.60, 4.25, 3.8, 65000000),
    ("TSLA", AssetClass.EQUITY, 298.50, 7.80, 2.9, 48000000),
    ("PLTR", AssetClass.EQUITY, 58.40, 9.15, 4.2, 52000000),
    ("SMCI", AssetClass.EQUITY, 32.80, -12.40, 5.1, 75000000),
    ("COIN", AssetClass.EQUITY, 275.20, 8.40, 3.1, 18000000),
    ("AAPL", AssetClass.EQUITY, 224.80, 0.65, 1.1, 38000000),
    ("MSFT", AssetClass.EQUITY, 425.10, 1.20, 0.9, 19000000),
    ("AMD", AssetClass.EQUITY, 148.90, 3.40, 2.2, 34000000),
    ("AMZN", AssetClass.EQUITY, 208.30, -0.45, 1.0, 26000000),
    ("META", AssetClass.EQUITY, 585.10, 2.10, 1.4, 14000000),
    ("GOOGL", AssetClass.EQUITY, 178.40, 0.85, 0.8, 17000000),
    ("MARA", AssetClass.EQUITY, 24.50, 14.80, 4.5, 39000000),

    # Crypto (L1s, High-Volume Alts)
    ("BTCUSDT", AssetClass.CRYPTO, 88450.0, 4.20, 2.4, 1850000000),
    ("ETHUSDT", AssetClass.CRYPTO, 3180.50, 2.80, 1.8, 890000000),
    ("SOLUSDT", AssetClass.CRYPTO, 214.20, 8.90, 3.6, 620000000),
    ("SUIUSDT", AssetClass.CRYPTO, 3.25, 18.50, 5.4, 410000000),
    ("DOGEUSDT", AssetClass.CRYPTO, 0.38, 22.40, 6.2, 980000000),
    ("AVAXUSDT", AssetClass.CRYPTO, 34.80, 5.60, 2.1, 140000000),
    ("NEARUSDT", AssetClass.CRYPTO, 5.80, 7.10, 2.8, 110000000),
    ("LINKUSDT", AssetClass.CRYPTO, 14.60, 3.40, 1.5, 95000000),

    # Futures Contracts
    ("ES", AssetClass.FUTURES, 5865.25, 0.75, 1.2, 1200000),
    ("NQ", AssetClass.FUTURES, 20850.50, 1.10, 1.4, 950000),
    ("GC", AssetClass.FUTURES, 2685.40, -0.80, 1.6, 320000),
    ("CL", AssetClass.FUTURES, 68.40, -1.90, 2.3, 580000),

    # Forex Majors
    ("EURUSD", AssetClass.FOREX, 1.0650, -0.35, 1.2, 14000000),
    ("GBPUSD", AssetClass.FOREX, 1.2840, -0.60, 1.5, 9800000),
    ("USDJPY", AssetClass.FOREX, 154.60, 0.85, 1.8, 12000000),
]


class UniverseRegistry:
    @staticmethod
    def get_instruments(asset_class: str = None) -> List[Tuple]:
        if not asset_class:
            return DEFAULT_UNIVERSE
        target = asset_class.upper().strip()
        return [inst for inst in DEFAULT_UNIVERSE if inst[1].value == target]

    @staticmethod
    def generate_synthetic_series(base_price: float, change_pct: float, bars_count: int = 25) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generates realistic OHLCV price series concluding at current market price and change %.
        """
        np.random.seed(abs(int(base_price * 100)) % 10000)
        daily_drift = (change_pct / 100.0) / bars_count
        noise = np.random.normal(daily_drift, 0.008, bars_count)

        # Build close series
        closes = [base_price * (1.0 - (change_pct / 100.0))]
        for ret in noise:
            closes.append(closes[-1] * (1.0 + ret))
        closes[-1] = base_price  # Anchor final price
        closes_arr = np.array(closes[1:], dtype=float)

        spread = base_price * 0.006
        highs = closes_arr + np.abs(np.random.normal(spread, spread * 0.5, bars_count))
        lows = closes_arr - np.abs(np.random.normal(spread, spread * 0.5, bars_count))
        volumes = np.random.uniform(50000, 250000, bars_count)

        return highs, lows, closes_arr, volumes


def get_default_universe():
    return DEFAULT_UNIVERSE
