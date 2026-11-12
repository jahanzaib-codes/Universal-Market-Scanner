# 🔍 Universal-Market-Scanner: Multi-Asset High-Throughput Screener Engine

[![CI & Code Quality](https://github.com/jahanzaib-codes/Universal-Market-Scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/jahanzaib-codes/Universal-Market-Scanner/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-brightgreen.svg)](https://fastapi.tiangolo.com)
[![Docker Ready](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

> **Real-time multi-asset market scanning engine covering US Equities, Futures, Forex, and Crypto. Evaluates Relative Volume (RVOL), multi-timeframe consolidation breakouts, VWAP deviations, and abnormal volatility surges across 10,000+ instruments.**

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│      Multi-Asset Data Feeds (Equities, Crypto, FX)     │
└───────────────────────────┬────────────────────────────┘
                            │ Real-Time Streaming Ticks
                            ▼
┌────────────────────────────────────────────────────────┐
│              Screener Processing Engine                │
│                                                        │
│  ┌──────────────────┐            ┌──────────────────┐  │
│  │   RVOL Engine    │            │   VWAP Deviation │  │
│  │ • 20D Time-of-Day│            │ • Sigma Bands    │  │
│  │ • Volume Surges  │            │ • Rebound Plays  │  │
│  └────────┬─────────┘            └────────┬─────────┘  │
│           │                               │            │
│           ▼                               ▼            │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Consolidation & Volatility Signals       │  │
│  │  • Donchian Channel Squeeze   • ATR(14) Surge    │  │
│  │  • Breakout / Breakdown       • Momentum Score   │  │
│  └────────────────────────┬─────────────────────────┘  │
└───────────────────────────┼────────────────────────────┘
                            │ Sub-10ms Ranked Results
         ┌──────────────────┴──────────────────┐
         ▼                                     ▼
┌─────────────────────────┐           ┌─────────────────────────┐
│ FastAPI REST API Engine │           │ Interactive Terminal    │
│ • POST /scan            │           │ CLI Suite (`cli.py`)    │
│ • GET /scan/breakouts   │           │ • Live Colorized Tables │
│ • GET /scan/rvol        │           │ • High-Speed Benchmarks │
└─────────────────────────┘           └─────────────────────────┘
```

---

## 🚀 Key Features

* **Sub-10ms High-Throughput Screening:** Vectorized algorithms screen hundreds of instruments per millisecond, filtering noise from institutional volume ignition.
* **Relative Volume (RVOL) Analytics:** Compares real-time cumulative volume against the 20-day historical time-of-day moving average. Detects institutional accumulation ($RVOL \ge 2.0x$).
* **Volume Weighted Average Price (VWAP) Tracking:** Computes intraday VWAP and standard deviation bands ($\pm 1\sigma, \pm 2\sigma$) to flag mean-reversion and momentum extension setups.
* **Consolidation Breakout Recognition:** Identifies multi-bar Donchian channel range squeezes and confirms breakout validity using volume and ATR expansion.
* **Composite Momentum Scoring:** Mathematical ranking (0.0 to 100.0) factoring in volume velocity, price trajectory, VWAP alignment, and breakout confirmation.
* **Multi-Asset Coverage:**
  * **US Equities:** Mega-caps, S&P 500, High Beta momentum runners (NVDA, TSLA, PLTR, COIN, SMCI).
  * **Crypto:** High-volume Layer 1s and token pairs (BTC, ETH, SOL, SUI, DOGE).
  * **Futures:** E-mini S&P (ES), Nasdaq 100 (NQ), Crude Oil (CL), Gold (GC).
  * **Forex:** Major currency pairs (EUR/USD, GBP/USD, USD/JPY).

---

## ⚡ Quickstart & Terminal Demonstration

### 1. Installation
```bash
git clone https://github.com/jahanzaib-codes/Universal-Market-Scanner.git
cd Universal-Market-Scanner
pip install -r requirements.txt
cp .env.example .env
```

### 2. Interactive Terminal Demo
Run the automated multi-asset screener suite:
```bash
python cli.py demo
```

```text
==========================================================================================
   🔍 UNIVERSAL-MARKET-SCANNER: HIGH-THROUGHPUT MULTI-ASSET ENGINE DEMO
==========================================================================================

[1/3] High-Momentum Multi-Asset Screen (RVOL >= 2.0x, Vol > $500k):
| Symbol   | Asset   | Price   | 24h Chg   | RVOL   | VWAP    | VWAP Dev   | Breakout Signal           |   Score |
|----------|---------|---------|-----------|--------|---------|------------|---------------------------|---------|
| MARA     | EQUITY  | $24.50  | +14.80%   | 4.5x   | $22.37  | +9.50%     | CONSOLIDATION_BREAKOUT_UP |   100   |
| COIN     | EQUITY  | $275.20 | +8.40%    | 3.1x   | $252.57 | +8.96%     | CONSOLIDATION_BREAKOUT_UP |    86.2 |
| SMCI     | EQUITY  | $32.80  | -12.40%   | 5.1x   | $33.87  | -3.15%     | NONE                      |    85   |
| SUIUSDT  | CRYPTO  | $3.25   | +18.50%   | 5.4x   | $3.05   | +6.52%     | NONE                      |    85   |
| PLTR     | EQUITY  | $58.40  | +9.15%    | 4.2x   | $56.06  | +4.17%     | NONE                      |    82.5 |
| TSLA     | EQUITY  | $298.50 | +7.80%    | 2.9x   | $286.88 | +4.05%     | CONSOLIDATION_BREAKOUT_UP |    82.4 |
| NVDA     | EQUITY  | $142.60 | +4.25%    | 3.8x   | $138.81 | +2.73%     | CONSOLIDATION_BREAKOUT_UP |    80.8 |
  ⚡ Screened 27 instruments in 7.19 ms.
```

### 3. Individual CLI Commands
```bash
# Scan equities for RVOL >= 2.0x
python cli.py scan --asset EQUITY --rvol 2.0

# Scan crypto pairs with high liquidity
python cli.py scan --asset CRYPTO --rvol 2.5 --limit 10

# Launch FastAPI web daemon
python cli.py serve --port 8000
```

---

## 📡 REST API Documentation

Start the server using `python main.py --serve` or `docker compose up -d`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Engine health status and supported asset classes. |
| `POST` | `/scan` | Execute a multi-factor scan with custom criteria (JSON body). |
| `GET` | `/scan/breakouts` | Return active consolidation breakout runners. |
| `GET` | `/scan/rvol` | Return top volume ignition surges ($RVOL \ge 3.0x$). |

Interactive OpenAPI documentation is live at `http://localhost:8000/docs`.

---

## 🐳 Docker Deployment

Deploy with Docker Compose:
```bash
docker compose up -d --build
```

---

## 👨‍💻 Author & Institutional Consulting

Developed by **Jahanzaib** — Quantitative Finance, Algorithmic Trading Systems, and AI Agent Architect.

* **Fiverr:** [https://www.fiverr.com/jahanzaib313110](https://www.fiverr.com/jahanzaib313110)
* **Telegram:** [@JanzebBlockdev](https://t.me/JanzebBlockdev)
* **GitHub:** [@jahanzaib-codes](https://github.com/jahanzaib-codes)

For custom screener integrations, institutional low-latency feeds, or proprietary factor screening, connect via Fiverr or Telegram.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
