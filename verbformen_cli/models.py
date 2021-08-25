from abc import ABC
from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel, Field


class PartOfSpeech(Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"


class Level(Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class NounForm(BaseModel):
    singular: str
    plural: str


class PageResult(BaseModel):
    search: str = Field(example="Schloss")
    text: str = Field(example="das Schloss")
    grammar: str = Field(example="Schlosses · Schlösser⁰")
    part_of_speech: PartOfSpeech = Field(example=PartOfSpeech.NOUN)
    level: Optional[Level] = Field(example=Level.A2)
    definitions: List[str] = Field(example=["bolt", "castle", "lock"])
    notes: List[str] = Field(example="⁰ Depends on meaning")
    summary: str = Field(description="paragraph above summary tile")


class Definition(BaseModel, ABC):
    search: str = Field(description="Search term")
    definitions: List[str]
    part_of_speech: PartOfSpeech
    text: str = Field(description="German dictionary word")
    level: Optional[Level] = Field(example=Level.A1, default=None)


class Declension(BaseModel):
    Nominative: str
    Accusative: str
    Dative: str
    Genitive: str
    title: str


class Noun(Definition):
    part_of_speech = PartOfSpeech.NOUN
    genitive: str
    plural: str
    genitive_ending: str
    plural_ending: str
    gender: str
    article: str

    declensions: List[Declension] = []


class Conjugation(BaseModel):
    title: str
    ich: str
    du: str
    er: str
    wir: str
    ihr: str
    sie: str


class Verb(Definition):
    part_of_speech = PartOfSpeech.VERB
    behavior: str = Field(example="regular")
    present: str = Field(example="holt")
    imperfect: str = Field(example="holte")
    perfect: str = Field(example="hat geholt")
    auxiliary_verb: str = Field(example="haben")
    secondary_auxiliary_verb: Optional[str] = Field(example="sein", default=None)
    flection: str = Field(example="Active")
    use: str = Field(example="Main")
    separable_prefix: str = Field(example="-fern for fernsehen", default=None)

    conjugations: List[Conjugation] = []


class Adjective(Definition):
    part_of_speech = PartOfSpeech.ADJECTIVE
    is_comparable: bool
    comparative: Optional[str] = None
    superlative: Optional[str] = None
    comparative_ending: Optional[str] = None
    superlative_ending: Optional[str] = None

    declensions: List[Declension] = []


class NotFound(BaseModel):
    search: str = Field(description="Search term")


SearchResult = Union[Definition, NotFound]
