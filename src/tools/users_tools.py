from typing import Dict, List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from uuid import UUID
from src.models.user_model import User
from langchain_core.tools import tool
from src.core.db import SessionLocal


@tool
def retrieve_user_by_id(user_id: str) -> dict | None:
    """
    Retrieve a User object by its ID.
    Returns a dictionary (name, email, id) or None if not found.
    """
    session: Session = SessionLocal()
    try:
        user_uuid = UUID(user_id)
        user = session.query(User).filter(User.id == user_uuid).first()
        if user:
            return {"id": str(user.id), "name": user.name, "email": user.email}
        return None
    except Exception as e:
        print(f"Error retrieving user by ID: {e}")
        return None
    finally:
        session.close()

 
@tool
def retrieve_user_name(arg: str) -> List[Dict] | None:
    """
    Retrieve users whose name or email contains the given string (case-insensitive).
    Returns a list of dictionaries (id, name, email) or None if no user found.
    """
    session: Session = SessionLocal()
    try:
        search_term = f"%{arg.strip().lower()}%"
        users = (
            session.query(User)
            .filter(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )
            .all()
        )
        if users:
            return [
            {"id": str(user.id), "name": user.name, "email": user.email}
            for user in users
        ]
        return None
    except Exception as e:
        print(f"Error retrieving user by name/email: {e}")
        return None
    finally:
        session.close()


