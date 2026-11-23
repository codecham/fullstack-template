from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

# Argon2: the current recommended algorithm for password hashing
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return a salted hash of the password, safe to store in the database."""
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Check a plain password against a stored hash."""
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    """Create a signed JWT that identifies `subject` (the user id) until it expires."""
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> str | None:
    """Return the subject (user id) of a valid token, or None if it is invalid or expired."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:  # bad signature, expired, malformed...
        return None
    subject = payload["sub"]
    return subject if isinstance(subject, str) else None
