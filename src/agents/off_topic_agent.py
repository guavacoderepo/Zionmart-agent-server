from src.schema.agent_schemes import AgentState
from langchain_core.messages import AIMessage


def off_topic(state:AgentState):
    msg = AIMessage(content=(
            "I’m not sure I can help with that question 😅. "
            "But don’t worry! I’m here to assist you with anything related to ZionMart’s products, "
            "orders, or shopping experience. Could you try asking about that?"
        )

    )
    # Append response to state messages
    state["messages"] = state.get("messages", []) + [msg]

    return state