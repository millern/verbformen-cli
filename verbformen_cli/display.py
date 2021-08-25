from typing import List

from rich.align import Align
from rich.console import Console
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from verbformen_cli.models import (
    Noun,
    Verb,
    Adjective,
    SearchResult,
    NotFound,
    Declension,
)

console = Console()
max_definitions = 5


def display_summary(result: SearchResult, include_tables: bool):
    if isinstance(result, NotFound):
        console.print(
            Panel(
                Text("No results found", justify="center"),
                title=result.search,
                expand=True,
            )
        )
        return
    elif isinstance(result, Noun):
        level = result.level.value if result.level else None
        gender = result.gender.capitalize()
        endings = f"Endings: {result.genitive_ending}/{result.plural_ending}"
        top_left = " • ".join([x for x in [level, gender, endings] if x])
        word = f"{result.article} {result.text}"
        details = f"{result.genitive} • {result.plural}"

        table = declension_table(result.declensions)

    elif isinstance(result, Verb):
        level = result.level.value if result.level else None
        auxiliary = f"{result.auxiliary_verb}" + (
            f" (also, {result.secondary_auxiliary_verb})"
            if result.secondary_auxiliary_verb
            else ""
        )
        top_left = f"{level} • {result.behavior} • {auxiliary}"
        word = result.text
        details = f"{result.present} • {result.imperfect} • {result.perfect}"
        table = conjugation_table(result.conjugations)
    elif isinstance(result, Adjective):
        top_left = (
            f"Endings: {result.comparative_ending}/{result.superlative_ending}"
            if result.is_comparable
            else ""
        )
        word = result.text
        details = (
            f"{result.text} • {result.comparative} • {result.superlative}"
            if result.is_comparable
            else f"{result.text} • -- • --"
        )
        table = declension_table(result.declensions)
    else:
        raise ValueError()
    group = Panel(
        Group(
            Text(top_left, style="dim"),
            Text(word, justify="center", style="bold"),
            Text(details, justify="center"),
            Text(""),
            Text(", ".join(result.definitions[0:max_definitions]), justify="center"),
        ),
        expand=False,
        title=result.search,
    )
    console.print(Align.center(group))
    if include_tables:
        console.print(Align.center(table))


def declension_table(declensions: List[Declension]) -> Table:
    t = Table()
    t.title = "Declensions"
    t.show_header = True
    t.add_column("")
    for d in declensions:
        t.add_column(d.title)

    t.add_row("Nominative", *[d.Nominative for d in declensions])
    t.add_row("Accusative", *[d.Accusative for d in declensions])
    t.add_row("Dative", *[d.Dative for d in declensions])
    t.add_row("Genitive", *[d.Genitive for d in declensions])
    return t


def conjugation_table(conjugations):
    t = Table()
    t.title = "Conjugations"
    t.show_header = True
    t.add_column("")
    for c in conjugations:
        t.add_column(c.title)
    t.add_row("ich", *[c.ich for c in conjugations])
    t.add_row("du", *[c.du for c in conjugations])
    t.add_row("er", *[c.er for c in conjugations])
    t.add_row("wir", *[c.wir for c in conjugations])
    t.add_row("ihr", *[c.ihr for c in conjugations])
    t.add_row("sie", *[c.sie for c in conjugations])
    return t
