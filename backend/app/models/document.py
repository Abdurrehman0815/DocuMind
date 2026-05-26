from sqlalchemy import DateTime, Integer, String, func, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="uploaded", nullable=False)
    extracted_text: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=True)
    extracted_entities = mapped_column(JSON, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
