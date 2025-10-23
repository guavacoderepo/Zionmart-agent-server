import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from src.core.db import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to tickets
    tickets = relationship("Ticket", back_populates="department")
