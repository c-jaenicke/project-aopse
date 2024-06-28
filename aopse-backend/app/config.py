import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def load_config():
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return Settings(openai_api_key=config["openai"]["api_key"])


settings = load_config()
