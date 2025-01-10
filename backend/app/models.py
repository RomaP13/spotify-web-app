from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class SpotifyToken(SQLModel, table=True):
    user_id: str | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_token: str = Field(max_length=300)
    refresh_token: str = Field(max_length=300)
    expires_in: datetime = Field()


class SpotifyTokenData(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
