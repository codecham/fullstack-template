from fastapi import APIRouter

from app.core.dependencies import CurrentUser
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_current_user(user: CurrentUser) -> UserRead:
    return UserRead.model_validate(user)
