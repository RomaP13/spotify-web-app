import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class SpotifyToken(SQLModel, table=True):
    user_session_id: uuid.UUID | None = Field(
        default=None, primary_key=True, index=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
    )
    access_token: str = Field(max_length=300)
    refresh_token: str = Field(max_length=300)
    expires_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False)
    )


class SpotifyTokenData(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
