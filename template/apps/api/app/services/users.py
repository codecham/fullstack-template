"""Business logic for users. Routes call these functions; they never build queries themselves."""

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models import User
from app.schemas.user import UserCreate

# Hash checked when the email is unknown, so a failed login takes the same time
# whether the account exists or not (otherwise timing reveals which emails exist)
_DUMMY_HASH = hash_password("dummy password used to equalize timing")


class EmailAlreadyRegisteredError(Exception):
    """Raised when creating a user whose email is already taken."""


def normalize_email(email: str) -> str:
    """Store emails in lowercase so Alice@Mail.com and alice@mail.com are the same."""
    return email.strip().lower()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == normalize_email(email)))


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        email=normalize_email(data.email),
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as error:  # the unique index on email rejected it
        db.rollback()
        raise EmailAlreadyRegisteredError(user.email) from error
    db.refresh(user)  # reload the values filled in by the database (created_at...)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Return the user if the email and password are correct, otherwise None."""
    user = get_user_by_email(db, email)
    if user is None:
        verify_password(password, _DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password) or not user.is_active:
        return None
    return user
