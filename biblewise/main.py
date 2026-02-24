"""Interactive terminal menu for Biblewise. Rich UI, scope, Games submenu."""

from biblewise.db import get_connection
from biblewise.games import run_hangman, run_memory_pairs, run_reference_quiz
from biblewise.scope import ScopeKind, scope_label
from biblewise.search import random_verse, search_by_reference, search_by_text
from biblewise.ui import (
    console,
    games_submenu,
    main_menu_choice,
    scope_menu,
    show_random_verse,
    show_search_results,
    show_single_verse,
    show_welcome,
)

SCOPE_DEFAULT: tuple[ScopeKind, int | None] = ("all", None)


def run(scope: tuple[ScopeKind, int | None]) -> tuple[ScopeKind, int | None] | None:
    """One iteration of main menu; returns updated scope, or None to quit."""
    scope_kind, book_position = scope
    choice = main_menu_choice(scope_kind, book_position)

    if choice in ("q", "quit"):
        return None

    try:
        conn = get_connection()
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        return scope

    if choice == "1":
        do_search(conn, scope_kind, book_position)
    elif choice == "2":
        do_random(conn, scope_kind, book_position)
    elif choice == "3":
        sub = games_submenu()
        if sub == "1":
            run_hangman(conn, scope_kind=scope_kind, book_position=book_position)
        elif sub == "2":
            run_memory_pairs(conn, scope_kind=scope_kind, book_position=book_position)
        elif sub == "3":
            run_reference_quiz(conn, scope_kind=scope_kind, book_position=book_position)
        elif sub and sub != "b":
            console.print("[yellow]Unknown option.[/yellow]")
    elif choice == "4":
        new_scope = scope_menu()
        if new_scope is not None:
            return new_scope
    else:
        if choice:
            console.print("[yellow]Unknown option.[/yellow]")

    return scope


def do_search(
    conn, scope_kind: ScopeKind, book_position: int | None
) -> None:
    from biblewise.ui import prompt_search

    raw = prompt_search()
    if not raw:
        return
    v = search_by_reference(conn, raw)
    if v:
        show_single_verse(v)
        return
    results = search_by_text(
        conn, raw, limit=10, scope_kind=scope_kind, book_position=book_position
    )
    show_search_results(results, raw)


def do_random(
    conn, scope_kind: ScopeKind, book_position: int | None
) -> None:
    v = random_verse(conn, scope_kind=scope_kind, book_position=book_position)
    show_random_verse(v)


def main() -> None:
    show_welcome()
    scope: tuple[ScopeKind, int | None] = SCOPE_DEFAULT

    while True:
        result = run(scope)
        if result is None:
            break
        scope = result
    console.print("\n[dim]Goodbye.[/dim]")


if __name__ == "__main__":
    main()
