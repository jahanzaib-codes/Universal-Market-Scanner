# Changelog

All notable changes to **Universal-Market-Scanner** are documented in this file.

## [1.0.0] - 2026-11-12
### Added
- High-throughput multi-asset screener engine (US Equities, Crypto, Futures, Forex).
- Real-time Relative Volume (RVOL) multiple calculation vs 20-day time-of-day baseline.
- Volume-Weighted Average Price (VWAP) calculation and standard deviation band deviation tracking.
- Vectorized Donchian range consolidation squeeze and volatility breakout detector.
- Composite quantitative Momentum Score algorithm (0 to 100 scale).
- FastAPI endpoints for programmatic screener integrations (`/scan`, `/scan/breakouts`, `/scan/rvol`).
- Interactive terminal screener suite (`python cli.py demo`, `python cli.py scan`).
- Multi-stage Docker containerization and GitHub Actions automated CI matrix.
