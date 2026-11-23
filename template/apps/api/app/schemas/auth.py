from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    """Returned after a successful login (OAuth2 access token response)."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"
    # Lifetime of the token in seconds, so clients know when it expires
    expires_in: int
