from verbformen_cli import parsers
from verbformen_cli.downloaders import (
    AbstractDownloader,
    create_search_url,
    CachedDownloader,
    Downloader,
)
from verbformen_cli.models import SearchResult, PartOfSpeech
from verbformen_cli.parsers import AbstractParser
from verbformen_cli.settings import settings


class VerbformenClient:
    def __init__(self, downloader: AbstractDownloader, parser: AbstractParser):
        self.downloader = downloader
        self.parser = parser

    def search(
        self, german_word: str, part_of_speech: PartOfSpeech = None
    ) -> SearchResult:
        url = create_search_url(german_word, part_of_speech)
        html = self.downloader.download(url)
        result = self.parser.parse_page(html)
        return result

    @classmethod
    def default_client(cls):
        downloader = CachedDownloader(settings.cache_dir, Downloader())
        parser = parsers.VerbformenParser()
        return VerbformenClient(downloader, parser)
