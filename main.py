

import sys
import io
import time
from rich.console import Console
from rich.panel import Panel

import monitor
import ai_advisor
import reporter

# Force UTF-8 output so Windows terminals don't crash on special characters
import io as _io
sys.stdout = _io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

console = Console()


def main() -> None:
    """
    Orchestrates the full pipeline: collect → analyse → display.
    Runs once and exits cleanly.
    """

    # ── Welcome Banner ──────────────────────────────────────────────────────
    console.print()
    console.print(Panel.fit(
        "[bold cyan]AI System Performance Tracker[/bold cyan]\n"
        "[dim]Powered by psutil + Google Gemini API[/dim]",
        border_style="cyan",
    ))

    # ── Step 1: Collect Metrics ─────────────────────────────────────────────
    console.print("\n[bold]Step 1/3 :[/bold] [cyan]Collecting system metrics...[/cyan]")


    start = time.time()
    try:
        metrics = monitor.collect_snapshot()
    except Exception as exc:
        console.print(f"\n[bold red]Failed to collect system metrics:[/bold red] {exc}")
        sys.exit(1)

    elapsed = round(time.time() - start, 2)
    console.print(f"[green]Done! Metrics collected in {elapsed}s[/green]")

    # Display what we collected
    reporter.print_metrics(metrics)
    reporter.print_processes(metrics["top_processes"])

    # ── Step 2: Send to Gemini API ──────────────────────────────────────────
    console.print("\n[bold]Step 2/3 :[/bold] [yellow]Sending data to Gemini AI... please wait[/yellow]")

    try:
        advice = ai_advisor.get_ai_advice(metrics)
    except ValueError as exc:
        console.print(f"\n[bold red]Configuration Error:[/bold red]\n{exc}")
        sys.exit(1)
    except Exception as exc:
        console.print(f"\n[bold red]Gemini API Error:[/bold red] {exc}")
        sys.exit(1)

    console.print("[green]AI analysis received![/green]")

    # ── Step 3: Display Advice ──────────────────────────────────────────────
    console.print("\n[bold]Step 3/3 :[/bold] [magenta]Displaying AI recommendations...[/magenta]")

    reporter.print_advice(advice)

    # ── Done ────────────────────────────────────────────────────────────────
    console.print()
    console.print(Panel.fit(
        "[bold green]Analysis Complete![/bold green]\n"
        "[dim]No data was stored. No background process is running.[/dim]",
        border_style="green",
    ))
    console.print()


if __name__ == "__main__":
    main()
