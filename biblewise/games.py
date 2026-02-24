"""Bible games: hangman, memory pairs, reference quiz. All respect scope."""

import random
import sqlite3

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from biblewise.scope import ScopeKind, scope_where_sql
from biblewise.search import random_verse

_console = Console()


def get_random_verse_for_game(
    conn: sqlite3.Connection,
    min_words: int = 5,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> dict | None:
    """Prefer verses with enough words; respects scope."""
    for _ in range(50):
        v = random_verse(conn, scope_kind=scope_kind, book_position=book_position)
        if v and len(v["text"].split()) >= min_words:
            return v
    return random_verse(conn, scope_kind=scope_kind, book_position=book_position)


def run_hangman(
    conn: sqlite3.Connection,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> None:
    verse = get_random_verse_for_game(
        conn, min_words=3, scope_kind=scope_kind, book_position=book_position
    )
    if not verse:
        _console.print("[red]No verses in database (or none in current scope).[/red]")
        return
    text = verse["text"]
    reference = verse["reference"]
    words = [w.strip(".,;:?!\"'") for w in text.split() if w.strip()]
    if not words:
        _console.print("[red]Verse has no words.[/red]")
        return
    target_word = random.choice([w for w in words if len(w) > 2])
    masked = "".join(c if c in " -'" else "_" for c in target_word)
    guessed = set()
    wrong = []
    max_wrong = 6

    _console.print()
    _console.print(
        Panel(
            f"[bold]Reference:[/bold] {reference}\n\n"
            "Guess the missing word from this verse.\n"
            "Type a [bold]letter[/bold] or the [bold]full word[/bold].",
            title="[bold cyan]Hangman[/bold cyan]",
            border_style="cyan",
        )
    )
    _console.print(f"\nWord: [bold]{masked}[/bold]  ({len(target_word)} letters)\n")

    while "_" in masked and len(wrong) < max_wrong:
        try:
            raw = Prompt.ask("Letter or word").strip().upper()
        except (EOFError, KeyboardInterrupt):
            _console.print()
            break
        if not raw:
            continue
        if len(raw) > 1:
            if raw == target_word.upper():
                _console.print("[green]Correct![/green]")
                masked = target_word
                break
            wrong.append(raw)
            _console.print(f"[red]Wrong.[/red] Mistakes: {wrong}")
            continue
        letter = raw[0]
        if letter in guessed:
            continue
        guessed.add(letter)
        if letter in target_word.upper():
            masked = "".join(
                c if c in " -'" or c.upper() in guessed else "_" for c in target_word
            )
            _console.print(f"[green]Good:[/green] {masked}")
        else:
            wrong.append(letter)
            _console.print(
                f"[red]No.[/red] Mistakes ({len(wrong)}/{max_wrong}): {', '.join(wrong)}"
            )

    _console.print()
    if "_" not in masked:
        _console.print(Panel(f"[green]Well done![/green] The word was \"{target_word}\".\n\n{reference}\n{text}", title="Verse", border_style="green"))
    else:
        _console.print(Panel(f"The word was \"{target_word}\".\n\n{reference}\n{text}", title="Verse", border_style="dim"))


def run_memory_pairs(
    conn: sqlite3.Connection,
    pairs: int = 4,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> None:
    """Match verse text to reference; respects scope."""
    where_extra, where_params = scope_where_sql(scope_kind, book_position)
    rows = conn.execute(
        f"""
        SELECT v.book_position, v.chapter, v.verse, v.text, b.name
        FROM verses v
        JOIN books b ON b.position = v.book_position
        WHERE LENGTH(v.text) BETWEEN 40 AND 120{where_extra}
        ORDER BY RANDOM()
        LIMIT ?
        """,
        (*where_params, pairs),
    ).fetchall()
    if len(rows) < 2:
        _console.print("[red]Not enough verses in scope for memory game (need at least 2).[/red]")
        return
    cards = []
    for r in rows:
        ref = f"{r[4]} {r[1]}:{r[2]}"
        text = (r[3][:60] + "…") if len(r[3]) > 60 else r[3]
        cards.append(("ref", ref))
        cards.append(("text", text))
    random.shuffle(cards)

    ref_indices = [i for i, (t, _) in enumerate(cards) if t == "ref"]
    text_indices = [i for i, (t, _) in enumerate(cards) if t == "text"]

    ref_table = Table(title="References", show_header=False)
    ref_table.add_column("Ref", style="cyan")
    ref_table.add_column("Reference", style="white")
    for i, idx in enumerate(ref_indices, 1):
        ref_table.add_row(str(i), cards[idx][1])
    text_table = Table(title="Verse snippets", show_header=False)
    text_table.add_column("Text", style="yellow")
    text_table.add_column("Snippet", style="white")
    for i, idx in enumerate(text_indices, 1):
        text_table.add_row(str(i), cards[idx][1])

    _console.print()
    _console.print(
        Panel(
            "Match each [cyan]Ref #[/cyan] to the correct [yellow]Text #[/yellow].\n"
            "Enter your guess as two numbers, e.g. [bold]1 3[/bold].",
            title="[bold cyan]Memory pairs[/bold cyan]",
            border_style="cyan",
        )
    )
    _console.print(ref_table)
    _console.print(text_table)

    ref_to_text = {}
    for r in rows:
        ref = f"{r[4]} {r[1]}:{r[2]}"
        ref_to_text[ref] = (r[3][:60] + "…") if len(r[3]) > 60 else r[3]
    correct = 0
    total = len(rows)
    while correct < total:
        try:
            line = Prompt.ask("\nYour pair (Ref# Text#)").strip()
        except (EOFError, KeyboardInterrupt):
            _console.print()
            break
        parts = line.split()
        if len(parts) != 2:
            _console.print("[yellow]Enter two numbers, e.g. 1 2[/yellow]")
            continue
        try:
            rn, tn = int(parts[0]), int(parts[1])
        except ValueError:
            _console.print("[yellow]Use numbers only.[/yellow]")
            continue
        if rn < 1 or rn > total or tn < 1 or tn > total:
            _console.print("[yellow]Numbers out of range.[/yellow]")
            continue
        ref_card = cards[ref_indices[rn - 1]][1]
        text_card = cards[text_indices[tn - 1]][1]
        if ref_to_text.get(ref_card) == text_card or ref_to_text.get(ref_card) == text_card.rstrip("…"):
            correct += 1
            _console.print("[green]Match![/green]")
        else:
            _console.print("[red]No match. Try again.[/red]")
    _console.print()
    if correct == total:
        _console.print("[bold green]All pairs matched![/bold green]")
    else:
        _console.print(f"[dim]Matched {correct}/{total} pairs.[/dim]")


def run_reference_quiz(
    conn: sqlite3.Connection,
    num_options: int = 4,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> None:
    """Show a verse and multiple references; choose the correct one. Respects scope."""
    verse = get_random_verse_for_game(
        conn, min_words=2, scope_kind=scope_kind, book_position=book_position
    )
    if not verse:
        _console.print("[red]No verses in database (or none in current scope).[/red]")
        return
    correct_ref = verse["reference"]
    options = [correct_ref]
    attempts = 0
    while len(options) < num_options and attempts < 100:
        other = random_verse(conn, scope_kind=scope_kind, book_position=book_position)
        if other and other["reference"] not in options:
            options.append(other["reference"])
        attempts += 1
    if len(options) < num_options:
        _console.print(f"[yellow]Only {len(options)} unique verses in scope; quiz will have fewer options.[/yellow]")
    random.shuffle(options)
    correct_index = options.index(correct_ref)

    snippet = verse["text"][:200] + ("…" if len(verse["text"]) > 200 else "")

    _console.print()
    _console.print(
        Panel(
            f'[italic]"{snippet}"[/italic]',
            title="[bold cyan]Reference quiz[/bold cyan] — Which reference is this verse from?",
            border_style="cyan",
        )
    )
    opt_table = Table(show_header=False)
    opt_table.add_column("Choice", style="cyan", width=4)
    opt_table.add_column("Reference", style="white")
    for i, ref in enumerate(options, 1):
        opt_table.add_row(str(i), ref)
    _console.print(opt_table)

    try:
        raw = Prompt.ask(f"\nYour choice (1–{num_options})")
        choice = int(raw)
    except (EOFError, KeyboardInterrupt, ValueError):
        _console.print()
        return
    if 1 <= choice <= num_options:
        if choice - 1 == correct_index:
            _console.print("[bold green]Correct![/bold green]")
        else:
            _console.print(f"[red]Wrong.[/red] It was: [bold]{correct_ref}[/bold]")
    else:
        _console.print("[yellow]Invalid number.[/yellow]")
