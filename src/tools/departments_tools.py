from langchain_core.tools import tool
from sqlalchemy.orm import Session
from typing import List, Dict
from src.models.department_model import Department
from src.core.db import SessionLocal

@tool
def get_department(name: str) -> List[Dict]:
    """
    Retrieve departments matching a name (case-insensitive, partial match).
    Returns a list of dictionaries with department id and name.
    """
    session: Session = SessionLocal()
    try:
        departments = (
            session.query(Department)
            .filter(Department.name.ilike(f"%{name}%"))
            .all()
        )
        return [{"id": str(d.id), "name": d.name} for d in departments]
    except Exception as e:
        print(f"Error retrieving department: {e}")
        return []
    finally:
        session.close()
