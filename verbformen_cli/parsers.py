import abc
import re
from typing import Optional, List, Dict

from verbformen_cli.models import (
    PartOfSpeech,
    Level,
    Noun,
    Verb,
    Adjective,
    SearchResult,
    NotFound,
    Declension,
    Conjugation,
)

from bs4 import BeautifulSoup


class ParseError(Exception):
    ...


class AbstractParser(abc.ABC):
    @abc.abstractmethod
    def parse_page(self, html: str) -> SearchResult:
        ...


class VerbformenParser(AbstractParser):
    def parse_page(self, html: str) -> SearchResult:
        soup = BeautifulSoup(html, "html.parser")
        search = self._parse_search(soup)
        if self._not_found(soup):
            return NotFound(**{"search": search})

        part_of_speech = self._parse_part_of_speech(soup)
        description = self._description_paragraph(soup, part_of_speech)
        definitions = {
            "definitions": self._parse_definitions(soup),
            "search": self._parse_search(soup),
        }
        if part_of_speech == PartOfSpeech.NOUN:
            return Noun(
                **self._extract_noun_data(description) | definitions,
                declensions=self._parse_declensions(soup, ["Singular", "Plural"]),
            )

        elif part_of_speech == PartOfSpeech.VERB:
            return Verb(
                **self._extract_verb_data(description) | definitions,
                conjugations=self._parse_conjugations(
                    soup, ["Present", "Imperfect", "Present Subj.", "Imperf. Subj."]
                ),
            )

        elif part_of_speech == PartOfSpeech.ADJECTIVE:
            return Adjective(
                **self._extract_adjective_data(description) | definitions,
                declensions=self._parse_declensions(
                    soup, ["Masculine", "Neutral", "Feminine", "Plural"]
                ),
            )
        else:
            raise ValueError()

    def _not_found(self, soup: BeautifulSoup) -> bool:
        content = soup.find("meta", attrs={"name": "description"})["content"]
        return "List of all words starting with the text" in content

    def _parse_part_of_speech(self, soup: BeautifulSoup) -> PartOfSpeech:
        meta = soup.find("meta", attrs={"name": "description"})["content"]
        if "Declension of noun" in meta:
            return PartOfSpeech.NOUN
        if "Conjugation German verb" in meta:
            return PartOfSpeech.VERB
        if "Declension and comparison of" in meta:
            return PartOfSpeech.ADJECTIVE
        raise ParseError(f"failed to parse meta: {meta}")

    def _description_paragraph(
        self, soup: BeautifulSoup, part_of_speech: PartOfSpeech
    ) -> str:
        """text of paragraph above the definition box"""

        if part_of_speech == PartOfSpeech.NOUN:
            regex = "declension of the noun"
        elif part_of_speech == PartOfSpeech.ADJECTIVE:
            regex = "declension of the adjective"
        elif part_of_speech == PartOfSpeech.VERB:
            regex = "conjugation of the verb"
        else:
            raise ValueError(f"unexpected PartOfSpeech: {part_of_speech}")

        return clean_whitespace(
            soup.find(text=re.compile(f".*{regex}.*")).parent.parent.get_text()
        )

    def _extract_noun_data(self, description) -> Dict[str, str]:
        regex = re.match(
            r"The declension of the noun (?P<text>\S+) is in singular genitive "
            r"(?P<genitive>\S+) and in the plural nominative (?P<plural>\S+). "
            r"The noun (?P=text) is declined with the declension endings "
            r"(?P<genitive_ending>\S+)/(?P<plural_ending>\S+?). "
            r"(?:It can also be used with other endings\. )?"
            r"(?:In the plural is an umlaut\. )?"
            r"(?:It does not form plurals\. )?"
            r"(?:In the plural forms of (?P<possible_plural>\S+?) are possible\. )?"
            r"The voice of (?P=text) is (?P<gender>[a-z]+) and the article "
            r'"(?P<article>(der)|(die)|(das))"\. '
            r"(?:The noun can also be used with other genus and other articles\. )?"
            r"Here you can not only inflect (?P=text) but also all German nouns\. "
            r"(?:The noun is part of the thesaurus of Zertifikat Deutsch respectivly "
            r"Level (?P<level>\w{2})\.)?",
            description,
        )
        if not regex:
            raise ParseError(f"Parse Error:\n{description}")
        return regex.groupdict()

    def _parse_declensions(
        self, soup: BeautifulSoup, titles: List[str]
    ) -> List[Declension]:
        return [
            Declension(**self._parse_verbformen_table(soup, title)) for title in titles
        ]

    def _parse_conjugations(
        self, soup: BeautifulSoup, titles: List[str]
    ) -> List[Conjugation]:
        return [
            Conjugation(**self._parse_verbformen_table(soup, title)) for title in titles
        ]

    def _parse_verbformen_table(self, soup, title: str) -> Dict[str, str]:
        """
        Parse declension or conjugation table under the header

        :param soup: BeautifulSoup of page
        :param title: title of the declension/conjugation (singular, masculine, present)
        :return:
        """
        rows = soup.find("h2", text=title).find_next_sibling("table").find_all("tr")

        d = {}
        for row in rows:
            th = row.find("th")
            if not th:
                key = row.find("td").get_text()
                value = " ".join([td.get_text() for td in row.find_all("td")[1:]])
            else:
                key = th["title"]
                value = " ".join([td.get_text() for td in row.find_all("td")])
            d[clean_whitespace(key)] = clean_whitespace(value)
        d["title"] = title
        return d

    def _extract_verb_data(self, description) -> Dict[str, str]:
        regex = re.match(
            r"^The conjugation of the verb (?P<text>\S+) is (?P<behavior>\S+)\. "
            r"Basic forms are (?P<present>[\S ]+), (?P<imperfect>[\S ]+) and "
            r"(?P<perfect>[\S ]+?)\. "  # non-greedy for optional next line
            r"(?:The stem vowels are ([\S ]+)\. )?"
            r"The auxiliary verb of (?P=text) is (?P<auxiliary_verb>\S+?)\. "
            r"(?:(?P<secondary_auxiliary_verb>\S+) can be used as well\. )?"
            r"(?:First syllable (?P<separable_prefix>[\S-]+) of "
            r"(?P=text) is separable\. )?"
            r"(?:Can also be used not separable\. )?"
            r"(?:Prefix (?P<nonseparable_prefix>[\S-]+) of (?P=text) is not"
            r" separable\. )?"
            r"The flection is in (?P<flection>\S+) and the use as (?P<use>\S+)\. "
            r"For a better understanding, countless examples of the verb (?P=text) are"
            r" available\. "
            r"For practicing and consolidating, there are also free worksheets for"
            r" (?P=text)\. "
            r"You can not just (?P=text) conjugate, but all German verbs\. "
            r"(?:The verb is part of the thesaurus of Zertifikat Deutsch respectivly"
            r" Level"
            r" (?P<level>\w{2})\.)?",
            description,
        )
        if not regex:
            raise ParseError(f"Parse Error:\n{description}")
        return regex.groupdict()

    def _extract_adjective_data(self, description):
        # incomparable adjectives
        if regex := re.match(
            r"The declension of the adjective (?P<text>\S+) uses the incomparable form"
            r" (?P=text). "
            r"The adjective has no forms for the comparative and superlative. "
            r"The adjective (?P=text) can be used both attributively in front of a noun"
            r" as well as predicative in conjunction with a verb."
            r"One can not only inflect and compare (?P=text), but all German"
            r" adjectives\.",
            description,
        ):
            return regex.groupdict() | {"is_comparable": False}

        # comparable adjectives
        if regex := re.match(
            r"The declension of the adjective (?P<text>\S+) uses these forms of the"
            r" comparison (?P=text),(?P<comparative>\S+),(?P<superlative>.+)\. "
            r"The endings for the comparison in the comparative and superlative are"
            r" (?P<comparative_ending>\S+)/(?P<superlative_ending>\S+). "
            r"The adjective (?P=text) can be used both attributively in front of a noun"
            r" as well as predicative in conjunction with a verb."
            r"One can not only inflect and compare (?P=text), but all German"
            r" adjectives\.",
            description,
        ):
            return regex.groupdict() | {"is_comparable": True}
        raise ParseError(f"Parse Error:\n{description}")

    def _parse_level(self, soup: BeautifulSoup) -> Optional[Level]:
        level = soup.find(title=re.compile("^Vocabulary Certificate"))
        if not level:
            return None
        return Level[clean_whitespace(level.text)]

    def _parse_definition(self, soup: BeautifulSoup) -> str:
        container = soup.find(class_="rAbschnitt")
        definition = clean_whitespace(container.select(".vGrnd.rCntr")[0].get_text())
        return definition

    def _parse_search(self, soup: BeautifulSoup):
        return clean_whitespace(soup.find("input", type="search")["value"])

    def _parse_grammar(self, soup: BeautifulSoup) -> str:
        return clean_whitespace(
            soup.find(class_="rAbschnitt").select(".vStm.rCntr")[0].get_text()
        )

    def _parse_definitions(self, soup: BeautifulSoup):
        # image next to english definitions, if they exist
        eng_marker = soup.find(class_="rAbschnitt").find("img", alt="English")
        if not eng_marker:
            return []
        return [clean_whitespace(x) for x in eng_marker.parent.get_text().split(",")]

    def _parse_notes(self, soup) -> List[str]:
        return [
            clean_whitespace(tag.get_text())
            for tag in soup.find(class_="rAbschnitt").select(".rInf.vLeg.rClear")
        ]


def clean_whitespace(text: str):
    if not text:
        return text
    return re.sub(r"\s+", " ", text).strip()
