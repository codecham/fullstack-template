from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.health import DatabaseHealthResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/db")
def get_health_db(db: Annotated[Session, Depends(get_db)]) -> DatabaseHealthResponse:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from error
    return DatabaseHealthResponse(database="ok")
