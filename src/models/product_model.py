import uuid
from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
