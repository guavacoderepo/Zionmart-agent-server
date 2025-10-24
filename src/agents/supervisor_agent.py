from langchain_google_genai import ChatGoogleGenerativeAI
from src.schema.agent_schemes import AgentState, SupervisorModel, OrderSupervisorModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") 

# --- Node 1: Query classifier ---
async def supervisor(state: AgentState):
    question = state.get('refine_question')
    system_prompt = """
        Classify the user's message into one of these categories:

        1. "order" — Anything about creating, updating, cancelling, or checking orders or about products.  
        2. "complaint" — Any issue, dissatisfaction, or support request.  
        3. "enquiry" — General questions about the company, services or policies.  
        4. "off_topic" — Unrelated to the store.

        Return only: order, complaint, enquiry, or off_topic.
    """

    classifier_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User question: {question}")
    ])

    structured_llm = llm.with_structured_output(SupervisorModel)
    classifier_llm = classifier_prompt | structured_llm
    result = await classifier_llm.ainvoke({"question": question})

    state["topic"] = result.status  # type: ignore
    return state

# --- Node 2: Order classifier ---
async def order_supervisor(state: AgentState):
    question = state.get("messages", "")[-1].content # type: ignore
    system_prompt = """
        You are a query classifier for an e-commerce assistant. 
        Classify the user’s message into one of the following categories:

        1. "create_order" — Placing a new order.
        2. "edit_order" — Updating or modifying an existing order.
        3. "cancel_order" — Cancelling or stopping an order.
        4. "retrieve_items" — Checking product availbilty or viewing products, prices, or item descriptions.

        Return only: create_order, edit_order, cancel_order, or retrieve_items.
    """
    order_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User question: {question}")
    ])

    structured_llm = llm.with_structured_output(OrderSupervisorModel)
    order_llm = order_prompt | structured_llm
    result = await order_llm.ainvoke({"question": question})

    state["order_type"] = result.status  # type: ignore
    return state