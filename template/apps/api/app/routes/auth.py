"""Account creation and login."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services import users

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"description": "Email already registered"}},
)
def register(data: UserCreate, db: Annotated[Session, Depends(get_db)]) -> UserRead:
    try:
        user = users.create_user(db, data)
    except users.EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from None
    return UserRead.model_validate(user)


@router.post(
    "/login",
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect email or password"}},
)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    # OAuth2 calls the field "username": we use it for the email
    user = users.authenticate_user(db, form.username, form.password)
    if user is None:
        # Same message whether the email or the password is wrong:
        # never tell an attacker which emails have an account
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(str(user.id)),
        expires_in=get_settings().access_token_expire_minutes * 60,
    )
