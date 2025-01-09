from datetime import datetime

from sqlmodel import Field, SQLModel


class SpotifyToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    spotify_user_id: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_token: str = Field(max_length=300)
    refresh_token: str = Field(max_length=300)
    expires_in: datetime = Field()
