import os
from typing import Dict, Optional
import yaml
from pydantic_settings import BaseSettings

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


class OpenAIConfig(BaseSettings):
    api_key: str
    model: str
    assistant_id: str


class TavilyConfig(BaseSettings):
    api_key: str


class AIAssistantConfig(BaseSettings):
    default_provider: str
    providers: Dict[str, OpenAIConfig]
    tools: Dict[str, TavilyConfig]


class BaseConfig(BaseSettings):
    aopse: AIAssistantConfig


class ConfigSingleton:
    _instance: Optional[BaseConfig] = None

    @classmethod
    def get_instance(cls, config_path: str = DEFAULT_CONFIG_PATH) -> BaseConfig:
        if cls._instance is None:
            cls._instance = cls._load_config(config_path)
        return cls._instance

    @classmethod
    def _load_config(cls, config_path: str) -> BaseConfig | None:
        try:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
            config = BaseConfig(**config_data)
            print(f"Configuration loaded successfully from '{config_path}'")
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in configuration file: {e}")
        except ValueError as e:
            print(f"Error: Invalid configuration data: {e}")
        return None

    @classmethod
    def save_config(cls, config: BaseConfig, config_path: str = DEFAULT_CONFIG_PATH):
        try:
            with open(config_path, "w") as f:
                yaml.dump(config.dict(), f)
            print(f"Configuration saved successfully to '{config_path}'")
        except IOError as e:
            print(f"Error: Unable to write to configuration file: {e}")


config = ConfigSingleton.get_instance()
