from pydantic import BaseModel, BaseSettings, validator
from typing import Optional, Dict, List
import yaml


class Channel(BaseModel):
    name: str
    type: str
    url: str
    include: List[str]
    exclude: List[str]


class Channels(BaseModel):
    channels: List[Channel]


class Environment(BaseSettings):
    """Settings class for the Connect Monitor application

    All args can be passed as environment variables.

    If a config path is provided, the application will attempt to load
    configuration from the file, which will override CHANNELS with the
    channels configured in the supplied configuration file.

    Args:
        CONNECT_URL (str): The URL of the Connect cluster
        ENVIRONMENT (str): The environment the application is running in
        LOG_LEVEL (str): The log level for the application
        LOG_FORMAT (str): The log format for the application
        CONFIG_PATH (optional<str>): The path to the configuration file
        CHANNELS (optional<Channels>): The channels to send messages to
    """

    CONNECT_URL: str = "http://localhost:8083"
    ENVIRONMENT: str = "dev"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"

    CONFIG_PATH: Optional[str] = None
    CHANNELS: Optional[Channels] = None

    def __str__(self) -> str:
        return f"Settings(CONNECT_URL={self.CONNECT_URL}, ENVIRONMENT={self.ENVIRONMENT}, LOG_LEVEL={self.LOG_LEVEL}, LOG_FORMAT={self.LOG_FORMAT}, CONFIG_PATH={self.CONFIG_PATH}, CHANNELS={self.CHANNELS})"

    def __repr__(self):
        return self.__str__()

    @validator("LOG_LEVEL", pre=True)
    def validate_log_level(cls, v: str):
        if v.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                "LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        return v.upper()

    @validator("CHANNELS", pre=True)
    def load_config(cls, v: Optional[str], values: Dict[str, any]):
        config_path = values.get("CONFIG_PATH")
        if config_path:
            with open(config_path, "r") as f:
                config: Channels = Channels(**yaml.safe_load(f))
                return config

    class Config:
        env_file = ".env"


env = Environment()
