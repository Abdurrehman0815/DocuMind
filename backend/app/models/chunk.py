from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.config.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # all-MiniLM-L6-v2 uses 384 dimensions
    embedding = mapped_column(Vector(384))
    
    # Optional relationship if needed
    # document = relationship("Document", backref="chunks")
