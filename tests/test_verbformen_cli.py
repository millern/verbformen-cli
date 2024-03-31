import pytest
from verbformen_cli import __version__
from verbformen_cli.clients import VerbformenClient
from verbformen_cli.downloaders import CachedDownloader, Downloader
from verbformen_cli.models import Level, Noun, Verb, Adjective, NotFound
from verbformen_cli.parsers import VerbformenParser
from verbformen_cli.settings import settings


def test_version():
    assert __version__ == "0.1.0"


def test_not_found():
    search = "zzz"
    result = download(search)
    assert isinstance(result, NotFound)


@pytest.mark.parametrize(
    "search,genitive,plural,genitive_ending,plural_ending,gender,article,level,"
    "first_definition",
    [
        (
            "Mädchen",
            "Mädchens",
            "Mädchen",
            "s",
            "-",
            "neutral",
            "das",
            Level.A1,
            "girl",
        ),
        (
            "Flugzeug",
            "Flugzeug(e)s",
            "Flugzeuge",
            "es",
            "e",
            "neutral",
            "das",
            Level.A1,
            "aircraft",
        ),
        (
            "Bedingung",
            "Bedingung",
            "Bedingungen",
            "-",
            "en",
            "feminine",
            "die",
            Level.B1,
            "condition",
        ),
        ("Hund", "Hund(e)s", "Hunde", "es", "e", "maskuline", "der", Level.A1, "dog"),
        (
            "Flughafen",
            "Flughafens",
            "Flughäfen",
            "s",
            "ä-",
            "maskuline",
            "der",
            Level.A1,
            "airport",
        ),
        ("Schlaf", "Schlaf(e)s", "-", "es", "-", "maskuline", "der", Level.A2, "sleep"),
        (
            "Holz",
            "Holzes",
            "Hölzer",
            "es",
            "ö-er",
            "neutral",
            "das",
            Level.A1,
            "wood",
        ),
        (
            "Kamin",
            "Kamin(e)s",
            "Kamine",
            "es",
            "e",
            "maskuline",
            "der",
            Level.C1,
            "fireplace",
        ),
        (
            "Aufbau",
            "Aufbau(e)s",
            "-",
            "es",
            "-",
            "maskuline",
            "der",
            Level.B2,
            "buildup",
        ),
        (
            "Gehalt",
            "Gehalt(e)s",
            "Gehalte",
            "es",
            "e",
            "maskuline",
            "der",
            Level.A2,
            "salary",
        ),
    ],
)
def test_nouns(
    search,
    genitive,
    plural,
    genitive_ending,
    plural_ending,
    gender,
    article,
    level,
    first_definition,
):

    result = download(search)
    assert isinstance(result, Noun)
    assert result.search == search
    assert result.text == search
    assert result.genitive == genitive
    assert result.plural == plural
    assert result.genitive_ending == genitive_ending
    assert result.plural_ending == plural_ending
    assert result.gender == gender
    assert result.article == article
    assert result.level == level
    assert result.definitions[0] == first_definition


@pytest.mark.parametrize(
    "search,behavior,present,imperfect,perfect,auxiliary_verb,flection,use,level,"
    "first_definition,separable_prefix,non_separable_prefix",
    [
        (
            "holen",
            "regular",
            "holt",
            "holte",
            "hat geholt",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "get",
            None,
            None,
        ),
        (
            "raten",
            "irregular",
            "rät",
            "riet",
            "hat geraten",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "recommend to do",
            None,
            None,
        ),
        (
            "lieben",
            "regular",
            "liebt",
            "liebte",
            "hat geliebt",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "love",
            None,
            None,
        ),
        (
            "schlagen",
            "irregular",
            "schlägt",
            "schlug",
            "hat geschlagen",
            "haben",
            "Active",
            "Main",
            Level.B1,
            "punch",
            None,
            None,
        ),
        (
            "essen",
            "irregular",
            "isst",
            "aß",
            "hat gegessen",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "dine",
            None,
            None,
        ),
        (
            "fernsehen",
            "irregular",
            "sieht fern",
            "sah fern",
            "hat ferngesehen",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "teleview",
            "fern-",
            None,
        ),
        (
            "nachschlagen",
            "irregular",
            "schlägt nach",
            "schlug nach",
            "hat nachgeschlagen",
            "haben",
            "Active",
            "Main",
            Level.B1,
            "look up",
            "nach-",
            None,
        ),
        (
            "ausleeren",
            "regular",
            "leert aus",
            "leerte aus",
            "hat ausgeleert",
            "haben",
            "Active",
            "Main",
            None,
            "empty (out)",
            "aus-",
            None,
        ),
        (
            "erzählen",
            "regular",
            "erzählt",
            "erzählte",
            "hat erzählt",
            "haben",
            "Active",
            "Main",
            Level.A1,
            "talk",
            None,
            None,
        ),
        (
            "durchfallen",
            "irregular",
            "fällt durch",
            "fiel durch",
            "ist durchgefallen",
            "sein",
            "Active",
            "Main",
            Level.B1,
            "flop",
            "durch-",
            None,
        ),
        (
            "umfassen",
            "regular",
            "umfasst",
            "umfasste",
            "hat umfasst",
            "haben",
            "Active",
            "Main",
            Level.B2,
            "grasp",
            None,
            "um-",
        ),
        (
            "umwenden",
            "irregular",
            "wendet um",
            "wandte um",
            "hat umgewandt",
            "haben",
            "Active",
            "Main",
            None,
            "turn",
            "um-",
            None,
        ),
    ],
)
def test_verbs(
    search,
    behavior,
    present,
    imperfect,
    perfect,
    auxiliary_verb,
    flection,
    use,
    level,
    first_definition,
    separable_prefix,
    non_separable_prefix,
):
    result = download(search)
    assert isinstance(result, Verb)
    assert result.search == search
    assert result.text == search
    assert result.behavior == behavior
    assert result.present == present
    assert result.imperfect == imperfect
    assert result.perfect == perfect
    assert result.auxiliary_verb == auxiliary_verb
    assert result.flection == flection
    assert result.use == use
    assert result.level == level
    assert result.definitions[0] == first_definition
    assert result.separable_prefix == separable_prefix


@pytest.mark.parametrize(
    "search,is_comparable,comparative,superlative,comparative_ending,"
    "superlative_ending",
    [
        ("glücklich", True, "glücklicher", "am glücklichsten", "er", "sten"),
        ("endlich", False, None, None, None, None),
    ],
)
def test_adjectives(
    search,
    is_comparable,
    comparative,
    superlative,
    comparative_ending,
    superlative_ending,
):
    result = download(search)
    assert isinstance(result, Adjective)
    assert result.search == search
    assert result.is_comparable == is_comparable
    assert result.comparative == comparative
    assert result.superlative == superlative
    assert result.comparative_ending == comparative_ending
    assert result.superlative_ending == superlative_ending


def download(word):
    downloader = CachedDownloader(settings.cache_dir, Downloader())
    client = VerbformenClient(downloader=downloader, parser=VerbformenParser())
    result = client.search(word)
    return result
