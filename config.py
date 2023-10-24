import os
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict

# env_dir = os.path.abspath("../..")
# print(env_dir)  # !1111111111111111111111111111111111111111111111111111111111
# env_file_path = os.path.join(env_dir, ".env")


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_password: str
    db_user: str
    fastapi_host: str
    fastapi_port: int
    fastapi_debug: bool
    fastapi_name: str = "Currency app"

    currency_name_url: str
    base_currency_url: str
    currency_api_version: str
    currency_names: str
    currency_rates: str

    # model_config = SettingsConfigDict(env_file=env_file_path)