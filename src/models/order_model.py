import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from src.core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")
    quantity = Column(Integer, nullable=False)  # total quantity for quick reference
    total = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to OrderItem
    items = relationship("OrderItem", back_populates="order")
