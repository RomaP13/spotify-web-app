from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    spotify_client_id: SecretStr
    spotify_client_secret: SecretStr
    redirect_uri: str
    # TODO: Maybe add building multihosturl from postgres credentials
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
