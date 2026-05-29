from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Any

console = Console()

def display_summary(start_date: str, end_date: str, agent_data: List[List[Any]], group_data: List[List[Any]]):
    # Agent Table
    table = Table(title=f"Performance de Agentes ({start_date} a {end_date})")
    table.add_column("Agente", style="cyan")
    table.add_column("Grupo", style="magenta")
    table.add_column("Chats", justify="right")
    table.add_column("Msgs", justify="right", style="bold cyan")
    table.add_column("ART (min)", justify="right")
    table.add_column("SLA", justify="right")
    table.add_column("NPS Real", justify="right")

    for row in agent_data:
        if row[2] == "TOTAIS": continue
        resp_time = row[14]
        sla = row[15]
        nps_real = row[13]
        color = "white"
        if isinstance(resp_time, (int, float)):
            color = "green" if resp_time <= 15 else ("yellow" if resp_time <= 30 else "red")
        table.add_row(str(row[2]), str(row[1]), str(row[3]), str(row[9]), f"[{color}]{resp_time}[/]", f"{sla}%", str(row[13]))

    console.print("\n")
    console.print(table)

    # Group Table
    gtable = Table(title=f"Performance por Grupo ({start_date} a {end_date})", border_style="magenta")
    gtable.add_column("Grupo", style="bold magenta")
    gtable.add_column("Chats", justify="right")
    gtable.add_column("Msgs", justify="right")
    gtable.add_column("ART Médio (min)", justify="right")
    gtable.add_column("SLA", justify="right")
    gtable.add_column("NPS Real", justify="right")

    for row in group_data:
        if row[0] == "TOTAIS": continue
        art = row[3]
        color = "white"
        if isinstance(art, (int, float)):
            color = "green" if art <= 15 else ("yellow" if art <= 30 else "red")
        gtable.add_row(str(row[0]), str(row[1]), str(row[2]), f"[{color}]{art}[/]", f"{row[4]}%", str(row[7]))

    console.print("\n")
    console.print(gtable)

def print_panel(message: str, title: str = "Info"):
    console.print(Panel(message, title=title))
