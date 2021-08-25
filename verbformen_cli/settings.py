import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    cache_dir: pathlib.Path = pathlib.Path(__file__).parents[1] / ".cache"


settings = Settings()
