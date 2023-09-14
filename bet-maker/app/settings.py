from functools import cache

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DATABASE: int
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PORT: int = 5432
    DATABASE_DB: str
    DATABASE_DRIVER: str
    DATABASE_PASSWORD: str

    @property
    def REDIS_DSN(self) -> RedisDsn:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"

    @property
    def POSTGRES_DSN(self) -> PostgresDsn:
        return f"{self.DATABASE_DRIVER}://{self.DATABASE_USER}:\
            {self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_DB}"


@cache
def get_settings() -> Settings:
    return Settings()
