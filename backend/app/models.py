import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class SpotifyToken(SQLModel, table=True):
    """Represents a Spotify authentication token associated with a user session.

    This model stores access and refresh tokens required for authenticating
    Spotify API requests.

    Attributes:
        user_session_id (UUID | None): The unique identifier for the user session.
            Acts as the primary key.
        created_at (datetime): The timestamp when the token record was created.
            Defaults to the current UTC time.
        access_token (str): The Spotify access token used for API requests.
        refresh_token (str): The token used to obtain a new access token.
        expires_at (datetime): The timestamp indicating when the access token expires.
            Stored as a timezone-aware datetime.
    """

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
    """Represents Spotify authentication token data received from the API.

    This model is used to parse and validate token responses from Spotify's
    authentication endpoints before storing them in the database.

    Attributes:
        access_token (str): The temporary token used for authenticated API requests.
        refresh_token (str): The token used to obtain a new access token when the current one expires.
        expires_in (int): The lifespan of the access token in seconds.
    """

    access_token: str
    refresh_token: str
    expires_in: int
