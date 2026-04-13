
from typing import Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


# ── Severity colour mapping ───────────────────────────────────────────────────

SEVERITY_STYLE: dict[str, str] = {
    "low":      "bold green",
    "medium":   "bold yellow",
    "high":     "bold red",
    "critical": "bold white on red",
}

PRIORITY_STYLE: dict[str, str] = {
    "high":   "red",
    "medium": "yellow",
    "low":    "green",
}


# ── Section: System Metrics ───────────────────────────────────────────────────

def print_metrics(metrics: dict[str, Any]) -> None:
    """
    Display a formatted summary of the collected system metrics.

    Args:
        metrics (dict): The snapshot from monitor.collect_snapshot().
    """
    cpu = metrics["cpu"]
    ram = metrics["ram"]
    disk = metrics["disk"]

    # --- CPU Panel ---
    cpu_color = "green" if cpu["overall_percent"] < 60 else (
        "yellow" if cpu["overall_percent"] < 85 else "red"
    )
    cpu_text = Text()
    cpu_text.append(f"  Overall Usage  : ", style="bold")
    cpu_text.append(f"{cpu['overall_percent']}%\n", style=cpu_color + " bold")
    cpu_text.append(f"  Physical Cores : {cpu['physical_cores']}\n")
    cpu_text.append(f"  Logical Cores  : {cpu['logical_cores']}\n")

    # --- RAM Panel ---
    ram_color = "green" if ram["percent_used"] < 70 else (
        "yellow" if ram["percent_used"] < 88 else "red"
    )
    ram_text = Text()
    ram_text.append(f"  Total          : {ram['total_gb']} GB\n")
    ram_text.append(f"  Used           : ", style="bold")
    ram_text.append(f"{ram['used_gb']} GB ({ram['percent_used']}%)\n", style=ram_color + " bold")
    ram_text.append(f"  Available      : {ram['available_gb']} GB\n")

    # --- Disk Panel ---
    disk_color = "green" if disk["percent_used"] < 80 else (
        "yellow" if disk["percent_used"] < 92 else "red"
    )
    disk_text = Text()
    disk_text.append(f"  Total          : {disk['total_gb']} GB\n")
    disk_text.append(f"  Used           : ", style="bold")
    disk_text.append(f"{disk['used_gb']} GB ({disk['percent_used']}%)\n", style=disk_color + " bold")
    disk_text.append(f"  Free           : {disk['free_gb']} GB\n")

    console.print()
    console.print(Panel(cpu_text, title="[bold cyan]CPU[/bold cyan]", border_style="cyan", expand=False, width=50))
    console.print(Panel(ram_text, title="[bold magenta]RAM[/bold magenta]", border_style="magenta", expand=False, width=50))
    console.print(Panel(disk_text, title="[bold blue]Disk (C:)[/bold blue]", border_style="blue", expand=False, width=50))


# ── Section: Top Processes Table ──────────────────────────────────────────────

def print_processes(processes: list[dict[str, Any]]) -> None:
    """
    Render the top 10 processes as a colour-coded Rich table.

    Args:
        processes (list[dict]): List of process dicts from monitor.get_top_processes().
    """
    table = Table(
        title="Top 10 Processes",
        box=box.ROUNDED,
        border_style="bright_black",
        header_style="bold white",
        show_lines=True,
    )

    table.add_column("Rank",     style="dim",  width=5,  justify="center")
    table.add_column("Name",     style="bold", width=28)
    table.add_column("PID",      style="dim",  width=8,  justify="center")
    table.add_column("CPU %",    width=8,                justify="right")
    table.add_column("RAM (MB)", width=10,               justify="right")

    for rank, proc in enumerate(processes, start=1):
        cpu_style = (
            "bold red" if proc["cpu_percent"] >= 20 else
            "yellow"   if proc["cpu_percent"] >= 10 else
            "green"
        )
        ram_style = (
            "bold red" if proc["ram_mb"] >= 1000 else
            "yellow"   if proc["ram_mb"] >= 500  else
            "green"
        )
        table.add_row(
            str(rank),
            proc["name"],
            str(proc["pid"]),
            Text(f"{proc['cpu_percent']}%", style=cpu_style),
            Text(f"{proc['ram_mb']}", style=ram_style),
        )

    console.print()
    console.print(table)


# ── Section: AI Advice ────────────────────────────────────────────────────────

def print_advice(advice: dict[str, Any]) -> None:
    """
    Display the AI-generated performance recommendations in a rich layout.

    Args:
        advice (dict): Parsed JSON advice from ai_advisor.get_ai_advice().
    """
    severity = advice.get("severity", "unknown").lower()
    score    = advice.get("overall_health_score", "?")
    summary  = advice.get("summary", "No summary provided.")
    recs     = advice.get("recommendations", [])
    warnings = advice.get("warnings", [])

    sev_style = SEVERITY_STYLE.get(severity, "bold white")

    # --- Health Score colour ---
    score_color = (
        "bold green"  if isinstance(score, int) and score >= 75 else
        "bold yellow" if isinstance(score, int) and score >= 50 else
        "bold red"
    )

    header_text = Text()
    header_text.append("  Severity  : ", style="bold")
    header_text.append(f"{severity.upper()}\n", style=sev_style)
    header_text.append("  Health    : ", style="bold")
    header_text.append(f"{score}/100\n", style=score_color)
    header_text.append(f"\n  {summary}\n")

    console.print()
    console.print(Panel(
        header_text,
        title="[bold yellow]AI Performance Analysis[/bold yellow]",
        border_style="yellow",
        width=70,
    ))

    # --- Warnings ---
    if warnings:
        console.print()
        warn_text = "\n".join(f"  WARNING: {w}" for w in warnings)
        console.print(Panel(warn_text, title="[bold red]WARNINGS[/bold red]",
                            border_style="red", width=70))

    # --- Recommendations ---
    if recs:
        console.print()
        console.rule("[bold yellow]Recommendations[/bold yellow]")
        for i, rec in enumerate(recs, start=1):
            priority  = rec.get("priority", "medium").lower()
            action    = rec.get("action", "N/A")
            reason    = rec.get("reason", "N/A")
            savings   = rec.get("expected_savings", "N/A")
            pri_style = PRIORITY_STYLE.get(priority, "white")

            rec_text = Text()
            rec_text.append(f"  [{priority.upper()}] ", style=pri_style + " bold")
            rec_text.append(f"{action}\n\n", style="bold white")
            rec_text.append(f"  Why    : {reason}\n", style="dim")
            rec_text.append(f"  Saves  : ", style="dim")
            rec_text.append(f"{savings}\n", style="bold green")

            console.print(Panel(
                rec_text,
                title=f"[bold]#{i}[/bold]",
                border_style=pri_style,
                width=68,
            ))
    else:
        console.print("\n[bold green]No recommendations - your system looks healthy![/bold green]\n")
