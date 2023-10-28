from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base project settings"""

    db_host: str
    db_port: int
    db_name: str
    db_password: str
    db_user: str
    fastapi_host: str
    fastapi_port: int
    fastapi_debug: bool
    fastapi_name: str = "Currency app"

    api_key: str
    base_currency_url: str
    currency_api_version: str
    currency_names: str
    currency_rates: str
    expiration_period: int

    model_config = SettingsConfigDict(env_file=".env")
