from datetime import datetime
from typing import Annotated, Any, List, Optional, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import add_messages

class ClassifierModel(BaseModel):
    """Query classification result: "order", "complaint", "enquiry" or "off_topic"."""
    status: str = Field(..., description='Category of the user query: "order", "complaint", "enquiry" or "off_topic"')


class OrderClassifier(BaseModel):
    """Query classification result: "create_order", "edit_order", "cancel_order", or "retrieve_items"."""
    status: str = Field(..., description='Category of the user query: "create_order", "edit_order", "cancel_order", or "retrieve_items"')

# --- Define agent state ---
class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    topic: Optional[str]
    refine_question: Optional[str]
    order_type: Optional[str]
    user_id: Optional[str]
    retriever: Optional[Any]

class PromptModel(BaseModel):
    prompt: str
    user_id: str

class AuthModel(BaseModel):
    email: str


class ResponseModel(BaseModel):
    status: bool = True
    payload: Optional[Any] = None
    msg: Optional[str] = None


class ProductModel(BaseModel):
    id: str
    name: str
    description: str | None = None
    price: float

class OrderModel(BaseModel):
    user_id: str
    status: str = "pending"
    quantity: int
    total: float
    created_at: datetime
