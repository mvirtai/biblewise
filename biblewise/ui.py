"""Rich-based terminal UI: menus, panels, tables, prompts.

All user-facing text and layout live here. Uses a single shared Console instance.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from biblewise.scope import ScopeKind, scope_label

console = Console()


def show_welcome() -> None:
    """Print the welcome panel with app title and short description."""
    console.print(
        Panel(
            "[bold]Biblewise[/bold] — Memorize verses and references.\n"
            "Search, random verse, and games. Use [bold]scope[/bold] to limit to OT, NT, or one book.",
            title="[bold blue]Welcome[/bold blue]",
            border_style="blue",
        )
    )


def main_menu_choice(
    scope_kind: ScopeKind, book_position: int | None
) -> str:
    """Show main menu and return the user's choice (1–4, q)."""
    scope_str = scope_label(scope_kind, book_position)
    console.print()
    console.print(Panel(
        f"  [bold]1.[/bold] Search verse (reference or text)\n"
        f"  [bold]2.[/bold] Random verse\n"
        f"  [bold]3.[/bold] Games\n"
        f"  [bold]4.[/bold] Set scope  [dim](current: {scope_str})[/dim]\n"
        f"  [bold]q.[/bold] Quit",
        title="[bold cyan]Menu[/bold cyan]",
        border_style="cyan",
    ))
    return Prompt.ask("\nChoice", default="1").strip().lower()


def games_submenu() -> str:
    """Show games submenu and return choice (1–3, b)."""
    console.print()
    console.print(Panel(
        "  [bold]1.[/bold] Hangman — guess the word from a verse\n"
        "  [bold]2.[/bold] Memory pairs — match reference ↔ verse\n"
        "  [bold]3.[/bold] Reference quiz — verse → choose reference\n"
        "  [bold]b.[/bold] Back",
        title="[bold cyan]Games[/bold cyan]",
        border_style="cyan",
    ))
    return Prompt.ask("Game", default="b").strip().lower()


def scope_menu() -> tuple[ScopeKind, int | None] | None:
    """Show scope menu; return (scope_kind, book_position) or None to cancel (keep current)."""
    console.print()
    console.print(Panel(
        "  [bold]1.[/bold] All (whole Bible)\n"
        "  [bold]2.[/bold] Old Testament\n"
        "  [bold]3.[/bold] New Testament\n"
        "  [bold]4.[/bold] Single book (pick from list)\n"
        "  [bold]b.[/bold] Back (keep current)",
        title="[bold cyan]Set scope[/bold cyan]",
        border_style="cyan",
    ))
    choice = Prompt.ask("Scope", default="b").strip().lower()
    if choice == "b":
        return None
    if choice == "1":
        return ("all", None)
    if choice == "2":
        return ("ot", None)
    if choice == "3":
        return ("nt", None)
    if choice == "4":
        from biblewise.books import BOOKS

        table = Table(title="Books", show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=4)
        table.add_column("Book", style="white")
        for pos, _id, name in BOOKS:
            table.add_row(str(pos), name)
        console.print(table)
        raw = Prompt.ask("Book number (1–66)")
        try:
            pos = int(raw)
            if 1 <= pos <= 66:
                return ("book", pos)
        except ValueError:
            pass
        console.print("[yellow]Invalid book number.[/yellow]")
        return None
    return None


def show_single_verse(verse: dict) -> None:
    """Print one verse in a panel with reference as title."""
    console.print()
    console.print(
        Panel(
            verse["text"],
            title=f"[bold]{verse['reference']}[/bold]",
            border_style="green",
        )
    )


def show_search_results(results: list[dict], query: str) -> None:
    """Print search results as a table; show a message if no results."""
    if not results:
        console.print("[yellow]No verses found.[/yellow]")
        return
    console.print()
    table = Table(title=f"Search: “{query[:40]}{'…' if len(query) > 40 else ''}”", header_style="bold")
    table.add_column("Reference", style="cyan", width=18)
    table.add_column("Text", style="white", max_width=60)
    for v in results:
        text = v["text"][:80] + ("…" if len(v["text"]) > 80 else "")
        table.add_row(v["reference"], text)
    console.print(table)


def show_random_verse(verse: dict | None) -> None:
    """Print a random verse panel, or an error message if verse is None."""
    if not verse:
        console.print("[red]No verses in database (or none in current scope).[/red]")
        return
    show_single_verse(verse)


def prompt_search() -> str:
    """Ask for a reference or search text; return trimmed input."""
    return Prompt.ask(
        "Reference (e.g. John 3:16) or search text",
        default="",
    ).strip()
