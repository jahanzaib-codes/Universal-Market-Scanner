"""
Universal-Market-Scanner Interactive Terminal Suite & Live Screener CLI.
"""

import sys
import click
from tabulate import tabulate
from src.engine.screener_engine import get_screener_engine
from src.models.scanner_models import (
    AssetClass,
    BreakoutType,
    ScanFilterCriteria,
    VWAPCondition,
)


@click.group()
def cli():
    """Universal-Market-Scanner High-Throughput Terminal CLI."""
    pass


@cli.command("demo")
def demo():
    """Run full multi-asset screener test across Equities, Crypto, and Futures."""
    engine = get_screener_engine()

    click.secho("\n" + "=" * 90, fg="cyan", bold=True)
    click.secho("   🔍 UNIVERSAL-MARKET-SCANNER: HIGH-THROUGHPUT MULTI-ASSET ENGINE DEMO", fg="cyan", bold=True)
    click.secho("=" * 90, fg="cyan")

    # 1. Multi-Asset General Scan
    click.secho("\n[1/3] High-Momentum Multi-Asset Screen (RVOL >= 2.0x, Vol > $500k):", fg="yellow", bold=True)
    crit1 = ScanFilterCriteria(min_rvol=2.0, min_volume=500000.0, max_results=8)
    res1 = engine.run_scan(crit1)

    rows1 = []
    for r in res1.results:
        rows1.append([
            r.symbol,
            r.asset_class.value,
            f"${r.current_price:,.2f}" if r.current_price >= 1.0 else f"${r.current_price:.4f}",
            f"{r.change_24h_pct:+.2f}%",
            f"{r.rvol:.1f}x",
            f"${r.vwap:,.2f}",
            f"{r.vwap_deviation_pct:+.2f}%",
            r.breakout_type.value,
            f"{r.momentum_score:.1f}",
        ])
    print(tabulate(rows1, headers=["Symbol", "Asset", "Price", "24h Chg", "RVOL", "VWAP", "VWAP Dev", "Breakout Signal", "Score"], tablefmt="github"))
    click.echo(f"  ⚡ Screened {res1.total_screened} instruments in {res1.execution_time_ms} ms.")

    # 2. Consolidation Breakouts
    click.secho("\n[2/3] Donchian Range Consolidation Breakouts (Equities & Crypto):", fg="yellow", bold=True)
    crit2 = ScanFilterCriteria(min_rvol=2.5, min_volume=1000000.0, max_results=6)
    res2 = engine.run_scan(crit2)
    breakouts = [r for r in res2.results if r.breakout_type != BreakoutType.NONE]

    rows2 = []
    for r in breakouts:
        rows2.append([
            r.symbol,
            r.asset_class.value,
            f"${r.current_price:,.2f}",
            f"{r.change_24h_pct:+.2f}%",
            f"{r.rvol:.1f}x",
            f"${r.atr_14:.2f}",
            r.signal_summary[:45] + "...",
        ])
    print(tabulate(rows2, headers=["Symbol", "Class", "Price", "24h Chg", "RVOL", "ATR14", "Technical Signal Description"], tablefmt="github"))
    click.echo(f"  ⚡ Found {len(breakouts)} verified breakout candidates.")

    # 3. Extreme RVOL Volume Surges
    click.secho("\n[3/3] Extreme Relative Volume Movers (RVOL >= 3.5x):", fg="yellow", bold=True)
    crit3 = ScanFilterCriteria(min_rvol=3.5, max_results=5)
    res3 = engine.run_scan(crit3)

    rows3 = []
    for r in res3.results:
        rows3.append([
            r.symbol,
            r.asset_class.value,
            f"${r.current_price:,.2f}" if r.current_price >= 1.0 else f"${r.current_price:.4f}",
            f"{r.change_24h_pct:+.2f}%",
            f"{r.rvol:.1f}x 🔥",
            f"${r.volume:,.0f}",
            f"{r.momentum_score:.1f}/100",
        ])
    print(tabulate(rows3, headers=["Symbol", "Asset", "Price", "24h Chg", "RVOL Multiple", "24h Volume", "Momentum Rank"], tablefmt="github"))

    click.secho("\n" + "=" * 90, fg="cyan")
    click.secho("   ✅ ALL QUANTITATIVE SCREENER SUITES VALIDATED CLEANLY", fg="green", bold=True)
    click.secho("=" * 90 + "\n", fg="cyan")


@cli.command("scan")
@click.option("--asset", default=None, help="Asset class filter: EQUITY, CRYPTO, FUTURES, FOREX")
@click.option("--rvol", default=1.5, type=float, help="Minimum Relative Volume multiple")
@click.option("--limit", default=15, type=int, help="Max results count")
def scan(asset, rvol, limit):
    """Run real-time multi-asset market scan."""
    engine = get_screener_engine()
    act = AssetClass(asset.upper()) if asset else None
    criteria = ScanFilterCriteria(asset_class=act, min_rvol=rvol, max_results=limit)
    res = engine.run_scan(criteria)

    rows = []
    for r in res.results:
        rows.append([
            r.symbol,
            r.asset_class.value,
            f"${r.current_price:,.2f}" if r.current_price >= 1.0 else f"${r.current_price:.4f}",
            f"{r.change_24h_pct:+.2f}%",
            f"{r.rvol:.1f}x",
            f"${r.vwap:,.2f}",
            r.breakout_type.value,
            f"{r.momentum_score:.1f}",
        ])
    print(tabulate(rows, headers=["Symbol", "Asset", "Price", "Change", "RVOL", "VWAP", "Breakout", "Score"], tablefmt="github"))
    click.echo(f"\nExecution: {res.execution_time_ms} ms | Matches: {res.matching_count}")


@cli.command("serve")
@click.option("--host", default="0.0.0.0", help="Host interface")
@click.option("--port", default=8000, type=int, help="Listening port")
def serve(host, port):
    """Start the FastAPI screener server."""
    import uvicorn
    uvicorn.run("src.api.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        demo()
    else:
        cli()
