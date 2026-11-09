from functools import lru_cache
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Учёт заказов кофейни"
    default_page_size: int = Field(default=10, ge=1)
    max_page_size: int = Field(default=50, ge=1)
    default_offset: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def check_page_sizes(self):
        if self.default_page_size > self.max_page_size:
            raise ValueError("DEFAULT_PAGE_SIZE не должен превышать MAX_PAGE_SIZE")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
