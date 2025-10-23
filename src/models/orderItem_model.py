import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.core.db import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationship
    order = relationship("Order", back_populates="items")
