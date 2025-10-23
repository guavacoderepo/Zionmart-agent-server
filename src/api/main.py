import os
from src.core.config import Settings
settings = Settings()  # type: ignore

os.environ["GOOGLE_API_KEY"] = str(settings.GOOGLE_API_KEY)

from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, status
from langchain_core.messages import HumanMessage
from src.schema.agent_schemes import AgentState, AuthModel, PromptModel, ResponseModel
from src.models.user_model import User
from langchain_core.runnables import RunnableConfig
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.models.order_model import Order
from src.models.product_model import Product
import asyncio
import json

from src.core.db import SessionLocal
from src.agents.init_agent import agent
from src.core.db import SessionLocal, engine, Base


# Step 1: Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic Customer Care Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Agentic Customer Care System is live!"}


def user_prompt(user_id, prompt) -> AgentState:
    return {
        "messages": [HumanMessage(content=prompt)],
        "user_id": user_id
    }


def thread_config(user_id: str) -> RunnableConfig:
    return RunnableConfig(configurable={"thread_id": user_id})

@app.post("/app/prompt", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def prompt(req: PromptModel):
    try:
        # ✅ Create state from user prompt
        state = user_prompt(req.user_id, req.prompt)
        config = thread_config(req.user_id)
        # ✅ Await agent invocation
        response = await agent.ainvoke(state, config=config)
        print("QUESTION:->", response["refine_question"])
        return ResponseModel(
            payload=response["messages"]
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    
@app.post("/app/stream")
async def prompt_stream(req: PromptModel):
    try:
        # Create state from user prompt
        state = user_prompt(req.user_id, req.prompt)
        config = thread_config(req.user_id)

        async def event_generator():
            # Stream agent output
            async for chunk in agent.astream(state, config=config):
                # Each chunk is a partial response; convert to JSON string
                yield f"data: {json.dumps({'message': chunk})}\n\n"
                await asyncio.sleep(0.01)  # tiny delay to allow streaming

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        return StreamingResponse(
            f"data: {json.dumps({'error': str(e)})}\n\n",
            media_type="text/event-stream"
        )

@app.post("/app/auth", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def auth(req: AuthModel):
    session: Session = SessionLocal()
    try:
        user = ( session.query(User)
            .filter(User.email == req.email.strip()).first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email not found"
            )
    
        return ResponseModel(
            payload={
                "id": str(user.id), 
                "name": user.name, 
                "email": user.email
            }
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST) 


@app.get("/app/products", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def products():
    session: Session = SessionLocal()
    try:
        products = session.query(Product)
            
        return ResponseModel(
            payload=[
                {
                    "id": str(p.id), "name": p.name,
                    "price": p.price, "description": p.description,
                }
                for p in products
            ]
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    
@app.get("/app/orders/{user_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def orders(user_id:str):
    session: Session = SessionLocal()
    try:
        orders = session.query(Order).filter(Order.user_id == user_id).all()

        if not orders:
            return ResponseModel(
                payload=[]
            )
            
        return ResponseModel(
            payload=[
                {
                    "id": str(order.id),
                    "status": order.status,
                    "quantity": order.quantity,
                    "total": order.total,
                    "created_at": order.created_at
                }
                for order in orders
            ]
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)