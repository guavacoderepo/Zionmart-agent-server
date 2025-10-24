import json
from src.schema.agent_schemes import AgentState
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools import tools

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def on_topic_router(state: AgentState):
    topic = state.get("topic")
    if topic == "order":
        return "order_classifier"
    elif topic == "complaint":
        return "complaint"
    elif topic == "enquiry":
        return "enquiry"
    else:
        return "off_topic"
    
def on_order_router(state: AgentState):
    order_type = state.get("order_type")
    if order_type == "create_order":
        return "create_order"
    elif order_type == "edit_order":
        return "edit_order"
    elif order_type == "cancel_order":
        return "cancel_order"
    elif order_type == "retrieve_items":
        return "retrieve_items"
    else: 
        return None


async def route_handler(state:AgentState, prompt:str):
    llm_with_tools = llm.bind_tools(tools=tools)
    messages: list[BaseMessage] = [HumanMessage(content=prompt)]

    while True:
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)
        # --- Handle tool calls ---
        if getattr(response, "tool_calls", None):
            print("🧠 Tool calls detected — executing tools...")
            for call in response.tool_calls: # type: ignore
                tool_name = call.get("name")
                args = call.get("args", {})

                tool_func = next((t for t in tools if t.name == tool_name), None)
                if not tool_func:
                    continue
                try:
                    result = await tool_func.ainvoke(args)
                    messages.append(AIMessage(content=str(result), name=tool_name))
                except Exception as e:
                    messages.append(AIMessage(content=f"Error executing {tool_name}: {e}"))

            continue  # Loop back to LLM for reasoning
        # --- No more tool calls ---
        print("✅ Conversation complete — no further tool calls.")
        break
    


    if not getattr(messages[-1], "content"):
        response = await llm_with_tools.ainvoke(messages)
        if response.content and isinstance(response.content[0], dict):
            ai_text = response.content[0].get("text", "Sorry, I don't have an answer.")
        else:
            ai_text = str(response.content[0]) if response.content else "Sorry, I don't have an answer."

        messages.append(AIMessage(content=ai_text))
    # Update state with the last LLM message
    state["messages"] = state.get("messages", []) + [messages[-1]]
    return state