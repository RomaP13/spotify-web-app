from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.api.utils.session_utils import get_user_session_id
from app.core.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
UserSessionDep = Annotated[UUID, Depends(get_user_session_id)]
