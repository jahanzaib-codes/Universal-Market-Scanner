"""
FastAPI application exposing real-time market scanning endpoints.
"""

from fastapi import FastAPI, Query
from src.engine.screener_engine import get_screener_engine
from src.models.scanner_models import (
    AssetClass,
    BreakoutType,
    ScanFilterCriteria,
    ScanResponse,
    VWAPCondition,
)

app = FastAPI(
    title="Universal-Market-Scanner API",
    description="High-Throughput Multi-Asset RVOL and Breakout Screener API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "Universal-Market-Scanner",
        "version": "1.0.0",
        "status": "ONLINE",
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "engine": "ScreenerEngine v1.0",
        "supported_assets": ["EQUITY", "CRYPTO", "FUTURES", "FOREX"],
    }


@app.post("/scan", response_model=ScanResponse)
def run_custom_scan(criteria: ScanFilterCriteria):
    """Execute a multi-factor scan against custom threshold filters."""
    engine = get_screener_engine()
    return engine.run_scan(criteria)


@app.get("/scan/breakouts", response_model=ScanResponse)
def get_consolidation_breakouts(
    asset_class: str = Query(None, description="Optional filter: EQUITY, CRYPTO, FUTURES, FOREX"),
    min_rvol: float = Query(2.0, description="Minimum Relative Volume multiple"),
):
    """Scan exclusively for high-volume consolidation breakouts."""
    engine = get_screener_engine()
    act = AssetClass(asset_class.upper()) if asset_class else None
    criteria = ScanFilterCriteria(
        asset_class=act,
        min_rvol=min_rvol,
        min_volume=100000.0,
        max_results=15,
    )
    raw = engine.run_scan(criteria)
    # Filter for active breakouts
    breakout_results = [r for r in raw.results if r.breakout_type != BreakoutType.NONE]
    raw.results = breakout_results
    raw.matching_count = len(breakout_results)
    return raw


@app.get("/scan/rvol", response_model=ScanResponse)
def get_high_rvol_movers(
    min_rvol: float = Query(3.0, description="Minimum Relative Volume multiple (e.g. 3.0x)"),
):
    """Scan for extreme relative volume surges indicating institutional accumulation."""
    engine = get_screener_engine()
    criteria = ScanFilterCriteria(
        min_rvol=min_rvol,
        min_volume=500000.0,
        max_results=20,
    )
    return engine.run_scan(criteria)
