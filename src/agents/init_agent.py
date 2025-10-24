from src.agents.off_topic_agent import off_topic
from .rewriter_agent import rewriter_node
from .supervisor_agent import supervisor, order_supervisor
from .order_agent import cancel_order, create_order, edit_order, retrieve_items
from .complaint_enquiry_agent import complaint, enquiry
from src.services.routers_service import on_order_router, on_topic_router

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.schema.agent_schemes import AgentState

graph = StateGraph(AgentState)
memory = MemorySaver()

# --- Node 3: End node ---
def end_node(state: AgentState):
    return state

# --- Add nodes ---
graph.add_node("rewriter", rewriter_node)
graph.add_node("supervisor", supervisor)
graph.add_node("order_supervisor", order_supervisor)

graph.add_node("enquiry", enquiry)
graph.add_node("complaint", complaint)
graph.add_node("off_topic", off_topic)

graph.add_node("create_order", create_order)
graph.add_node("edit_order", edit_order)
graph.add_node("cancel_order", cancel_order)
graph.add_node("retrieve_items", retrieve_items)

graph.add_node("end", end_node)

graph.add_conditional_edges("order_supervisor", on_order_router)
graph.add_conditional_edges("supervisor", on_topic_router)

graph.add_edge("create_order", "end")
graph.add_edge("edit_order", "end")
graph.add_edge("cancel_order", "end")
graph.add_edge("retrieve_items", "end")
graph.add_edge("off_topic", "end")

# --- Define graph entry and exit ---
graph.set_entry_point("rewriter")
graph.add_edge("rewriter", "supervisor")
# graph.add_edge("order", END)
graph.add_edge("end", END)

# --- Compile app ---
agent = graph.compile(checkpointer=memory)
