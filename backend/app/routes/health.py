from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.database import get_db
from fastapi import Depends

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
