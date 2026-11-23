import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Data sent by the client to create an account."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    """Data sent back to the client. Never includes the password."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
