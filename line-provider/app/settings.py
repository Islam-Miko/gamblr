from functools import cache

from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: int

    @property
    def REDIS_DSN(self) -> RedisDsn:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"


@cache
def get_settings() -> Settings:
    return Settings()
