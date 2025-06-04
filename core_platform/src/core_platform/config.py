import os
import logging
from typing import Any, Literal
import json
import yaml
from pydantic import BaseModel, model_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthCredentialsConfig(BaseModel):
    username: str
    password: str

class ProductCatalogLegacyConfig(BaseModel):
    base_url: str

class AppConfig(BaseSettings):
    auth: dict[Literal['credentials'], list[AuthCredentialsConfig]]
    legacy_systems: dict[Literal['product_catalog'], ProductCatalogLegacyConfig]

    model_config = SettingsConfigDict(
        env_prefix='CORE_',
        env_file='.env',
        extra='ignore'
    )
    
    @model_validator(mode='before')
    @classmethod
    def load_config_file(cls, values: dict) -> dict:
        config_path = values.pop('config_path', None) or os.getenv('CONFIG_PATH', 'config/config.yaml')
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    file_values = yaml.safe_load(f)
                if file_values:  # Merge with any passed values
                    return {**file_values, **values}
            except Exception as e:
                raise ValueError(f"Error parsing config file: {e}")
        return values

def get_app_config() -> AppConfig:
    try:
        return AppConfig()
    except (ValidationError, ValueError) as e:
        logging.error(f"Invalid configuration: {e}")
        raise
