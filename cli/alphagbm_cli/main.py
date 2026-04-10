"""
AlphaGBM CLI — command entry point.

Usage:
    alphagbm stock analyze TICKER [--style balanced] [--json]
    alphagbm stock quote TICKER [--json]
    alphagbm options score TICKER [--strategy sell-put] [--expiry 2026-04-17] [--json]
    alphagbm options recommend [--count 5] [--json]
    alphagbm config set-key YOUR_API_KEY
    alphagbm config set-url http://localhost:5000
    alphagbm config show
"""

import json as json_mod
import sys
import click
from . import __version__

# ── Root group ─────────────────────────────────────────────────────────────

@click.group()
@click.version_option(__version__, prog_name="alphagbm")
def cli():
    """AlphaGBM — Stock & Options Analysis from the terminal."""
    pass


# ── Stock commands ─────────────────────────────────────────────────────────

@cli.group()
def stock():
    """Stock analysis commands."""
    pass


@stock.command("analyze")
@click.argument("ticker")
@click.option("--style", "-s", default="balanced",
              type=click.Choice(["quality", "value", "growth", "momentum", "balanced"]),
              help="Analysis style (default: balanced)")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def stock_analyze(ticker: str, style: str, as_json: bool):
    """Run a full stock analysis for TICKER."""
    from .client import post, AlphaGBMError
    from .display import display_stock_analysis, display_error, console

    try:
        with console.status(f"Analyzing {ticker.upper()}…", spinner="dots"):
            result = post(
                "/api/stock/analyze-sync",
                {"ticker": ticker.upper(), "style": style},
                timeout=90,
            )
    except AlphaGBMError as e:
        display_error(e.detail)
        sys.exit(1)

    if as_json:
        click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("success") is False:
            display_error(result.get("error", "Analysis failed"))
            sys.exit(1)
        display_stock_analysis(result)


@stock.command("quote")
@click.argument("ticker")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def stock_quote(ticker: str, as_json: bool):
    """Quick stock quote for TICKER (no quota cost)."""
    from .client import get, AlphaGBMError
    from .display import display_quick_quote, display_error

    try:
        result = get(f"/api/stock/quick-quote/{ticker.upper()}")
    except AlphaGBMError as e:
        display_error(e.detail)
        sys.exit(1)

    if as_json:
        click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("success") is False:
            display_error(result.get("error", "Quote failed"))
            sys.exit(1)
        display_quick_quote(result)


# ── Options commands ───────────────────────────────────────────────────────

@cli.group()
def options():
    """Options analysis commands."""
    pass


@options.command("score")
@click.argument("ticker")
@click.option("--strategy", "-s", default="all",
              type=click.Choice(["sell-put", "sell-call", "buy-call", "buy-put", "all"]),
              help="Strategy to score (default: all)")
@click.option("--expiry", "-e", default=None, help="Expiry date YYYY-MM-DD (auto-selects if omitted)")
@click.option("--top", "-n", default=5, type=int, help="Number of recommendations (max 10)")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def options_score(ticker: str, strategy: str, expiry: str, top: int, as_json: bool):
    """Score options for TICKER and return top recommendations."""
    from .client import post, AlphaGBMError
    from .display import display_options_score, display_error, console

    body = {
        "ticker": ticker.upper(),
        "strategy": strategy.replace("-", "_"),
        "top_n": min(top, 10),
    }
    if expiry:
        body["expiry_date"] = expiry

    try:
        with console.status(f"Scoring {ticker.upper()} options…", spinner="dots"):
            result = post("/api/v1/options/score", body, timeout=90)
    except AlphaGBMError as e:
        display_error(e.detail)
        sys.exit(1)

    if as_json:
        click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("success") is False:
            display_error(result.get("error", "Scoring failed"))
            sys.exit(1)
        display_options_score(result)


@options.command("recommend")
@click.argument("ticker", required=False, default=None)
@click.option("--count", "-n", default=5, type=int, help="Number of recommendations")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def options_recommend(ticker: str | None, count: int, as_json: bool):
    """Get daily options recommendations (or for a specific TICKER)."""
    from .client import get, AlphaGBMError
    from .display import display_options_recommend, display_error

    try:
        params = {"count": min(count, 10)}
        result = get("/api/options/recommendations", params=params)
    except AlphaGBMError as e:
        display_error(e.detail)
        sys.exit(1)

    if as_json:
        click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("success") is False:
            display_error(result.get("error", "Fetch failed"))
            sys.exit(1)
        display_options_recommend(result)


@options.command("snapshot")
@click.argument("ticker")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def options_snapshot(ticker: str, as_json: bool):
    """Quick IV/VRP snapshot for TICKER (no quota cost)."""
    from .client import get, AlphaGBMError
    from .display import console, display_error

    try:
        result = get(f"/api/options/snapshot/{ticker.upper()}")
    except AlphaGBMError as e:
        display_error(e.detail)
        sys.exit(1)

    if as_json:
        click.echo(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return

    if result.get("success") is False:
        display_error(result.get("error", "Snapshot failed"))
        sys.exit(1)

    from rich.table import Table
    from rich import box
    tbl = Table(title=f"{ticker.upper()} IV Snapshot", box=box.ROUNDED, show_header=False)
    tbl.add_column("Metric", style="cyan")
    tbl.add_column("Value", justify="right")

    tbl.add_row("Price", f"${result.get('price', 0):,.2f}" if result.get('price') else "N/A")
    tbl.add_row("Nearest Expiry", result.get("nearest_expiry", "—"))
    atm_iv = result.get("atm_iv")
    tbl.add_row("ATM IV", f"{atm_iv*100:.1f}%" if atm_iv else "—")
    tbl.add_row("IV Rank", f"{result.get('iv_rank', 0):.1f}" if result.get("iv_rank") is not None else "—")
    hv = result.get("hv_30d")
    tbl.add_row("HV 30d", f"{hv*100:.1f}%" if hv else "—")
    vrp = result.get("vrp")
    vrp_level = result.get("vrp_level", "")
    if vrp is not None:
        color = "green" if vrp > 0.05 else ("red" if vrp < -0.05 else "yellow")
        tbl.add_row("VRP", f"[{color}]{vrp*100:+.1f}%  ({vrp_level})[/{color}]")
    else:
        tbl.add_row("VRP", "—")

    console.print(tbl)


# ── Config commands ────────────────────────────────────────────────────────

@cli.group()
def config():
    """Manage CLI configuration."""
    pass


@config.command("set-key")
@click.argument("api_key")
def config_set_key(api_key: str):
    """Set your AlphaGBM API key."""
    from .config import load_config, save_config
    cfg = load_config()
    cfg["api_key"] = api_key
    save_config(cfg)
    masked = api_key[:8] + "…" + api_key[-4:] if len(api_key) > 16 else api_key[:8] + "…"
    click.echo(f"✅ API key saved: {masked}")


@config.command("set-url")
@click.argument("url")
def config_set_url(url: str):
    """Set the AlphaGBM API base URL."""
    from .config import load_config, save_config
    cfg = load_config()
    cfg["base_url"] = url.rstrip("/")
    save_config(cfg)
    click.echo(f"✅ Base URL saved: {cfg['base_url']}")


@config.command("show")
def config_show():
    """Show current configuration."""
    from .config import load_config, CONFIG_FILE
    cfg = load_config()
    click.echo(f"Config file: {CONFIG_FILE}")
    key = cfg.get("api_key", "")
    if key:
        masked = key[:8] + "…" + key[-4:] if len(key) > 16 else key[:8] + "…"
    else:
        masked = "(not set)"
    click.echo(f"API Key:     {masked}")
    click.echo(f"Base URL:    {cfg.get('base_url', '(not set)')}")


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
