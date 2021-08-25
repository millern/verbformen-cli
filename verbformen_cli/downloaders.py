import abc
import pathlib
import urllib.parse

import requests

from verbformen_cli.models import PartOfSpeech


class DownloaderError(Exception):
    ...


class AbstractDownloader(abc.ABC):
    @abc.abstractmethod
    def download(self, url: str) -> str:
        ...


class Downloader(AbstractDownloader):
    def download(self, url: str) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise DownloaderError()
        return response.text


class CachedDownloader(AbstractDownloader):
    def __init__(self, cache_path: pathlib.Path, delegate: AbstractDownloader):
        self.delegate = delegate
        self.cache_dir = cache_path
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str) -> str:
        path = self.cache_dir / urllib.parse.quote(url, safe="")
        if not path.is_file():
            page = self.delegate.download(url)
            path.write_text(page)
        return path.read_text()


def create_search_url(german_word: str, part_of_speech: PartOfSpeech = None) -> str:
    if part_of_speech == PartOfSpeech.NOUN:
        base = "https://www.verbformen.com/declension/nouns/?w="
    elif part_of_speech == PartOfSpeech.VERB:
        base = "https://www.verbformen.com/conjugation/?w="
    else:
        base = "https://www.verbformen.com/?w="
    return f"{base}{german_word}"
