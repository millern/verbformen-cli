import click

from verbformen_cli import clients
from verbformen_cli.display import display_summary
from verbformen_cli.models import PartOfSpeech


@click.command()
@click.argument("german_word")
@click.option(
    "--verb", "hint_pos", flag_value=PartOfSpeech.VERB.value, help="hint this is a verb"
)
@click.option(
    "--noun", "hint_pos", flag_value=PartOfSpeech.NOUN.value, help="hint this is a noun"
)
@click.option("--include_tables")
def lookup(german_word: str, hint_pos: str = None, include_tables: bool = False):
    """
    Lookup a word in the verbformen.net dictionary.

    If the part of speech is ambiguous, specify it using --noun or --verb

    """
    part_of_speech_hint = PartOfSpeech[hint_pos.upper()] if hint_pos else None
    client = clients.VerbformenClient.default_client()
    result = client.search(german_word, part_of_speech_hint)
    display_summary(result, include_tables)
