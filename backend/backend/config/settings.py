from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=False
    )

    mqtt_broker_url: str = Field(
        default="test.mosquitto.org",
        description="MQTT broker hostname (without protocol for aiomqtt)",
    )
    mqtt_broker_port: int = Field(
        default=8081, description="MQTT broker WebSocket port number"
    )
    mqtt_broker_path: str = Field(
        default='/mqtt', description="The WebSocket path for MQTT connection"
    )

    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


settings = Settings()
