"""Rich display helpers for CLI output."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()
err_console = Console(stderr=True)


# ── Stock display ──────────────────────────────────────────────────────────

def display_quick_quote(data: dict):
    """Display a quick stock quote."""
    ticker = data.get("ticker", "?")
    price = data.get("price", 0)
    change = data.get("change")
    pct = data.get("change_pct")
    name = data.get("name", ticker)

    change_str = ""
    if change is not None and pct is not None:
        color = "green" if change >= 0 else "red"
        sign = "+" if change >= 0 else ""
        change_str = f"  [{color}]{sign}{change:.2f} ({sign}{pct:.2f}%)[/{color}]"

    console.print(f"\n[bold]{name}[/bold] ({ticker}){change_str}")

    tbl = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    tbl.add_column("Label", style="dim")
    tbl.add_column("Value")

    tbl.add_row("Price", f"${price:,.2f}")
    if data.get("pe_ratio"):
        tbl.add_row("PE (TTM)", f"{data['pe_ratio']:.1f}")
    if data.get("forward_pe"):
        tbl.add_row("PE (Fwd)", f"{data['forward_pe']:.1f}")
    if data.get("market_cap"):
        mc = data["market_cap"]
        if mc >= 1e12:
            tbl.add_row("Market Cap", f"${mc/1e12:.2f}T")
        elif mc >= 1e9:
            tbl.add_row("Market Cap", f"${mc/1e9:.2f}B")
        else:
            tbl.add_row("Market Cap", f"${mc/1e6:.0f}M")
    if data.get("52w_high") and data.get("52w_low"):
        tbl.add_row("52-Week", f"${data['52w_low']:.2f} — ${data['52w_high']:.2f}")
    if data.get("sector"):
        tbl.add_row("Sector", data["sector"])

    console.print(tbl)


def display_stock_analysis(result: dict):
    """Display full stock analysis."""
    data = result.get("data", {})
    risk = result.get("risk", {})
    report = result.get("report", "")
    ev = data.get("ev_model", {})
    rec = ev.get("recommendation", {})

    ticker = data.get("symbol") or data.get("name", "?")
    price = data.get("price", 0)
    target = data.get("target_price", 0)
    stop = data.get("stop_loss_price", 0)

    # Header
    action = rec.get("action", "HOLD")
    confidence = rec.get("confidence", "")
    action_colors = {
        "STRONG_BUY": "bold green", "BUY": "green",
        "HOLD": "yellow",
        "AVOID": "red", "STRONG_AVOID": "bold red",
    }
    ac = action_colors.get(action, "white")
    console.print(f"\n[bold]{ticker}[/bold]  [{ac}]{action}[/{ac}]  (confidence: {confidence})")

    # Key metrics table
    tbl = Table(title="Key Metrics", box=box.ROUNDED, show_header=True)
    tbl.add_column("Metric", style="cyan")
    tbl.add_column("Value", justify="right")

    tbl.add_row("Price", f"${price:,.2f}" if price else "N/A")
    if target:
        upside = ((target - price) / price * 100) if price else 0
        color = "green" if upside > 0 else "red"
        tbl.add_row("Target Price", f"${target:,.2f}  [{color}]({upside:+.1f}%)[/{color}]")
    if stop:
        tbl.add_row("Stop Loss", f"${stop:,.2f}")

    risk_score = risk.get("score", 0)
    risk_level = risk.get("level", "?")
    risk_color = "green" if risk_score < 4 else ("yellow" if risk_score < 6 else "red")
    tbl.add_row("Risk Score", f"[{risk_color}]{risk_score:.1f}/10 ({risk_level})[/{risk_color}]")

    pos = risk.get("suggested_position")
    if pos is not None:
        tbl.add_row("Position Size", f"{pos:.1f}%")

    sentiment = data.get("market_sentiment")
    if sentiment is not None:
        tbl.add_row("Sentiment", f"{sentiment:.1f}/10")

    ev_score = ev.get("ev_score")
    ev_pct = ev.get("ev_weighted_pct") or ev.get("ev_extended_pct")
    if ev_score is not None:
        ev_str = f"{ev_score:.1f}/10"
        if ev_pct is not None:
            ev_str += f"  (EV: {ev_pct:+.2f}%)"
        tbl.add_row("EV Score", ev_str)

    console.print(tbl)

    # AI report (truncated)
    if report and isinstance(report, str):
        lines = report.strip()[:1500]
        console.print(Panel(lines, title="AI Analysis", border_style="blue", expand=False))


# ── Options display ────────────────────────────────────────────────────────

def display_options_score(result: dict):
    """Display options scoring results."""
    ticker = result.get("ticker", "?")
    strategy = result.get("strategy", "?")
    price = result.get("current_price", 0)
    expiry = result.get("expiry_date", "?")
    trend = result.get("trend", {})

    trend_dir = trend.get("direction", "?")
    trend_emoji = {"uptrend": "📈", "downtrend": "📉", "sideways": "➡️"}.get(trend_dir, "❓")

    console.print(f"\n[bold]{ticker}[/bold]  ${price:,.2f}  {trend_emoji} {trend_dir}")
    console.print(f"Strategy: [cyan]{strategy}[/cyan]  Expiry: {expiry}\n")

    # If strategy == 'all', iterate over strategies
    if strategy == "all":
        strategies = result.get("strategies", {})
        for strat_name, recs in strategies.items():
            if recs:
                _print_recs_table(strat_name, recs)
    else:
        recs = result.get("recommendations", [])
        _print_recs_table(strategy, recs)


def _print_recs_table(strategy_name: str, recs: list):
    """Print a recommendation table for one strategy."""
    if not recs:
        console.print(f"  [dim]No recommendations for {strategy_name}[/dim]\n")
        return

    tbl = Table(title=strategy_name.replace("_", " ").upper(), box=box.ROUNDED)
    tbl.add_column("#", style="dim", width=3)
    tbl.add_column("Strike", justify="right")
    tbl.add_column("DTE", justify="right", width=4)
    tbl.add_column("Score", justify="right")
    tbl.add_column("Yield%", justify="right")
    tbl.add_column("Safety%", justify="right")
    tbl.add_column("ATR", justify="center", width=5)
    tbl.add_column("Style", width=14)
    tbl.add_column("Win%", justify="right", width=5)

    for rec in recs:
        score = rec.get("score", 0)
        sc = "green" if score >= 70 else ("yellow" if score >= 50 else "red")

        atr_safe = rec.get("atr_safety", {})
        atr_str = "✅" if atr_safe.get("is_safe") else ("⚠️" if atr_safe else "—")

        ann_ret = rec.get("annualized_return_pct")
        ann_str = f"{ann_ret:.1f}" if ann_ret is not None else "—"

        safety = rec.get("safety_margin_pct")
        safety_str = f"{safety:.1f}" if safety is not None else "—"

        style = rec.get("style", "")
        win_prob = rec.get("win_probability")
        win_str = f"{win_prob:.0%}" if win_prob is not None else "—"

        tbl.add_row(
            str(rec.get("rank", "")),
            f"${rec.get('strike', 0):,.1f}" if rec.get("strike") else "—",
            str(rec.get("days_to_expiry", "—")),
            f"[{sc}]{score:.0f}[/{sc}]",
            ann_str,
            safety_str,
            atr_str,
            style,
            win_str,
        )

    console.print(tbl)
    console.print()


def display_options_recommend(result: dict):
    """Display daily options recommendations."""
    recs = result.get("recommendations", [])
    if not recs:
        console.print("[dim]No recommendations available.[/dim]")
        return

    console.print(f"\n[bold]Daily Options Recommendations[/bold]  ({len(recs)} picks)\n")

    for i, rec in enumerate(recs, 1):
        symbol = rec.get("symbol", "?")
        strategy = rec.get("strategy", "?")
        score = rec.get("score", 0)
        console.print(f"  {i}. [bold]{symbol}[/bold] — {strategy}  (score: {score:.0f})")

    summary = result.get("market_summary", {})
    if summary:
        console.print(f"\n  Market: VIX={summary.get('vix', '?')}  Outlook={summary.get('outlook', '?')}")


# ── Utility ────────────────────────────────────────────────────────────────

def display_error(msg: str):
    err_console.print(f"[red]Error:[/red] {msg}")
