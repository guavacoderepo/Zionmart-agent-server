from typing import List, Dict
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from src.core.db import SessionLocal
from src.models.product_model import Product


@tool
def retrieve_product_by_name(name: str) -> List[Dict]:
    """
    Retrieve products whose name partially matches the given input (case-insensitive).
    Returns a list of product dictionaries (id, name, price, description).
    """
    session: Session = SessionLocal()
    try:
        products = (
            session.query(Product)
            .filter(Product.name.ilike(f"%{name}%"))
            .all()
        )

        if not products:
            return [{"message": "No products found matching the given name"}]

        return [
            {
                "id": str(p.id), "name": p.name,
                "price": p.price, "description": p.description,
            }
            for p in products
        ]
    except Exception as e:
        print(f"Error retrieving product: {e}")
        return [{"error": str(e)}]
    finally:
        session.close()
