from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.api.utils.session_utils import get_user_session_id

UserSessionDep = Annotated[UUID, Depends(get_user_session_id)]
