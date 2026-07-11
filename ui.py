import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.status import Status

console = Console()


def print_header():
    console.print(
        Panel.fit(
            "[bold cyan]IT Support Digital Twin[/bold cyan]\n"
            "[dim]Your offline IT support assistant[/dim]",
            border_style="cyan",
        )
    )


def print_success(message: str):
    console.print(f"[bold green]{message}[/bold green]")


def print_warning(message: str):
    console.print(f"[bold yellow]{message}[/bold yellow]")


def print_error(message: str):
    console.print(f"[bold red]{message}[/bold red]")


def print_info(message: str):
    console.print(f"[cyan]{message}[/cyan]")


def prompt(message: str) -> str:
    return console.input(f"[cyan]{message}[/cyan]")


def confirm(message: str) -> bool:
    answer = console.input(f"[cyan]{message} [y/N]: [/cyan]").strip().lower()
    return answer == "y"


def spinner(message: str, delay: float = 0.8):
    """Context manager wrapper: `with spinner('Checking...'):` runs a dots
    spinner, then holds briefly to simulate processing."""

    class _Spinner:
        def __enter__(self):
            self._status = Status(message, spinner="dots", console=console)
            self._status.start()
            return self._status

        def __exit__(self, exc_type, exc_val, exc_tb):
            time.sleep(delay)
            self._status.stop()
            return False

    return _Spinner()


def render_table(title: str, columns: list[str], rows: list[list[str]]):
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)
