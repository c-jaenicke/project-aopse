import os
from typing import Dict

import yaml
from pydantic_settings import BaseSettings

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


class OpenAIConfig(BaseSettings):
    api_key: str
    model: str
    assistant_id: str


class AIAssistantConfig(BaseSettings):
    default_provider: str
    providers: Dict[str, OpenAIConfig]


class BaseConfig(BaseSettings):
    aopse: AIAssistantConfig


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> BaseConfig | None:
    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        return BaseConfig(**config_data)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in configuration file: {e}")
    except ValueError as e:
        print(f"Error: Invalid configuration data: {e}")
    return None


def save_config(config: BaseConfig, config_path: str = DEFAULT_CONFIG_PATH):
    try:
        with open(config_path, "w") as f:
            yaml.dump(config.dict(), f)
        print(f"Configuration saved successfully to '{config_path}'")
    except IOError as e:
        print(f"Error: Unable to write to configuration file: {e}")


try:
    config = load_config()
    if config is not None:
        print("Configuration loaded successfully")
    else:
        print("Failed to load configuration")
except Exception as e:
    print(f"An unexpected error occurred: {e}")