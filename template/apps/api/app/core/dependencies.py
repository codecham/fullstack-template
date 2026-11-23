import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import User
from app.services import users

# Reads the "Authorization: Bearer <token>" header.
# tokenUrl tells the /docs "Authorize" button where to log in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Return the logged-in user, or answer 401 if the token is missing or invalid."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subject = decode_access_token(token)
    if subject is None:
        raise unauthorized
    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise unauthorized from None
    user = users.get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise unauthorized
    return user


# Shortcut for routes: `def route(user: CurrentUser)`
CurrentUser = Annotated[User, Depends(get_current_user)]
