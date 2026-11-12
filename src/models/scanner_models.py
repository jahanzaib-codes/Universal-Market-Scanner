"""
Pydantic schemas for multi-asset screener criteria, price bars, and scanning results.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AssetClass(str, Enum):
    EQUITY = "EQUITY"
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    FUTURES = "FUTURES"


class BreakoutType(str, Enum):
    NONE = "NONE"
    CONSOLIDATION_BREAKOUT_UP = "CONSOLIDATION_BREAKOUT_UP"
    CONSOLIDATION_BREAKDOWN = "CONSOLIDATION_BREAKDOWN"
    VWAP_CROSS_ABOVE = "VWAP_CROSS_ABOVE"
    VOLATILITY_EXPANSION = "VOLATILITY_EXPANSION"


class VWAPCondition(str, Enum):
    ANY = "ANY"
    ABOVE_VWAP = "ABOVE_VWAP"
    BELOW_VWAP = "BELOW_VWAP"
    EXTREME_DEVIATION_UP = "EXTREME_DEVIATION_UP"
    EXTREME_DEVIATION_DOWN = "EXTREME_DEVIATION_DOWN"


class ScanFilterCriteria(BaseModel):
    asset_class: Optional[AssetClass] = None
    min_price: float = Field(default=1.0, description="Minimum price filter in USD")
    max_price: float = Field(default=5000.0, description="Maximum price filter in USD")
    min_volume: float = Field(default=200000.0, description="Minimum 24h/daily volume")
    min_rvol: float = Field(default=1.5, description="Relative Volume multiple vs 20-day historical average")
    vwap_condition: VWAPCondition = Field(default=VWAPCondition.ANY)
    min_change_pct: Optional[float] = Field(default=None, description="Minimum 24h price change percentage")
    max_results: int = Field(default=20, description="Maximum number of items to return")


class MarketBar(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class ScannerResult(BaseModel):
    symbol: str
    asset_class: AssetClass
    current_price: float
    change_24h_pct: float
    volume: float
    rvol: float
    vwap: float
    vwap_deviation_pct: float
    atr_14: float
    breakout_type: BreakoutType
    momentum_score: float  # Composite metric from 0.0 to 100.0
    signal_summary: str
    timestamp: str


class ScanResponse(BaseModel):
    scan_id: str
    total_screened: int
    matching_count: int
    execution_time_ms: float
    results: List[ScannerResult] = Field(default_factory=list)
    timestamp: str
