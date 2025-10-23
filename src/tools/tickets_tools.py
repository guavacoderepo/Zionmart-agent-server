from typing import Dict, Optional
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from src.core.db import SessionLocal
from src.models.ticket_model import Ticket

@tool
def create_ticket(user_id: str, subject: str, message: str, 
    department_id: Optional[str] = None
) -> Dict:
    """
    Create a new support ticket.
    Returns ticket details.
    """
    session: Session = SessionLocal()
    try:
        ticket = Ticket(
            user_id=user_id,
            subject=subject,
            message=message,
            department_id=department_id,
            status="open"
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return {
            "id": str(ticket.id),
            "user_id": str(ticket.user_id),
            "department_id": str(ticket.department_id),
            "subject": ticket.subject,
            "message": ticket.message,
            "status": ticket.status
        }
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def edit_ticket(
    ticket_id: str,
    subject: Optional[str] = None,
    message: Optional[str] = None,
    status: Optional[str] = None,
    department_id: Optional[str] = None,
) -> Dict:
    """
    Edit an existing ticket.
    Only provided fields will be updated.
    """
    session: Session = SessionLocal()
    try:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return {"error": "Ticket not found"}

        # Fields to update
        updates = {
            "subject": subject,
            "message": message,
            "status": status,
            "department_id": department_id
        }

        # Update only provided fields
        for attr, value in updates.items():
            if value is not None:
                setattr(ticket, attr, value)

        session.commit()
        session.refresh(ticket)
        return {
            "id": str(ticket.id),
            "subject": ticket.subject,
            "message": ticket.message,
            "status": ticket.status,
            "department_id": str(ticket.department_id),
            "updated_at": str(ticket.updated_at),
        }
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


@tool
def delete_ticket(ticket_id: str) -> Dict:
    """
    Delete a ticket by ID.
    Returns success or error message.
    """
    session: Session = SessionLocal()
    try:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return {"error": "Ticket not found"}

        session.delete(ticket)
        session.commit()
        return {"message": f"Ticket {ticket_id} deleted successfully"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()
