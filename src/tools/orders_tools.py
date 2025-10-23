from typing import Dict, List
from langchain_core.tools import tool
from sqlalchemy import func
from src.models.order_model import Order
from src.models.orderItem_model import OrderItem
from src.core.db import SessionLocal
import uuid


@tool
def create_order(user_id: str,  quantity:int, total:float=0.0) -> Dict:
    """
    Create a new order for a user.
    Quantity and total will be updated after adding items.
    """
    session = SessionLocal()
    try:
        status = 'pending'
        new_order = Order(id=str(uuid.uuid4()), total=total, user_id=user_id, status=status,quantity=quantity)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return {"id": new_order.id, "total":new_order.total, "user_id": new_order.user_id, "status": status, "quantity": quantity}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def add_order_item(order_id: str, product_id: str, quantity: int, price: float) -> Dict:
    """Add a new item to an existing order"""
    session = SessionLocal()
    try:
        item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return {"id": item.id, "product_id": item.product_id, "quantity": item.quantity, "price": item.price}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def edit_order_item(item_id: str, quantity: int) -> Dict:
    """Edit quantity of an existing order item."""
    session = SessionLocal()
    try:
        item = session.query(OrderItem).filter(OrderItem.id == item_id).first()
        if not item:
            return {"error": "Order item not found"}

        if quantity is not None:
            setattr(item, "quantity", quantity)

        session.commit()
        return {"id": item.id, "quantity": item.quantity}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def delete_order_item(item_id: str) -> Dict:
    """Delete a specific order item."""
    session = SessionLocal()
    try:
        item = session.query(OrderItem).filter(OrderItem.id == item_id).first()
        if not item:
            return {"error": "Order item not found"}

        session.delete(item)
        session.commit()
        return {"message": "Order item deleted successfully"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def delete_order(order_id: str) -> Dict:
    """Delete an order and all its items."""
    session = SessionLocal()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"error": "Order not found"}

        session.delete(order)
        session.commit()
        return {"message": "Order and its items deleted successfully"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def update_order(order_id: str, total:float, status: str) -> Dict:
    """
    Update the order's total price, status, and quantity.
    Returns the updated order details or an error message if the order is not found.
    """
    session = SessionLocal()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"error": "Order not found"}

        # Update fields if provided
        if status is not None:
            setattr(order, "status", status)
        if total is not None:
            setattr(order, "total", total)
        
        # Update quantity based on order items
        total_quantity = (
            session.query(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .with_entities(func.sum(OrderItem.quantity))
            .scalar()
        )

        setattr(order, "quantity", total_quantity or 0)

        session.commit()
        session.refresh(order)
        return {"id": str(order.id), "total": order.total, "status": order.status, "quantity": order.quantity}

    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def get_orders_by_user_id(user_id: str) -> List[Dict]:
    """
    Retrieve all orders belonging to a specific user.
    Returns a list of order dictionaries with id, status, and quantity.
    """
    session = SessionLocal()
    try:
        orders = session.query(Order).filter(Order.user_id == user_id).all()
        if not orders:
            return [{"message": "No orders found for this user"}]

        result = [
            {
                "id": str(order.id),
                "status": order.status,
                "quantity": order.quantity,
                "total": order.total,
            }
            for order in orders
        ]
        return result
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        session.close()


@tool
def get_order_items_by_order_id(order_id: str) -> List[Dict]:
    """
    Retrieve all order items for a specific order.
    Returns a list of dictionaries with item details.
    """
    session = SessionLocal()
    try:
        items = session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if not items:
            return [{"message": "No items found for this order"}]

        result = [
            {
                "id": str(item.id),
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price": item.price
            }
            for item in items
        ]
        return result
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        session.close()

