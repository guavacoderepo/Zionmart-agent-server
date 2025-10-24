from src.schema.agent_schemes import AgentState
from langchain_core.messages import AIMessage


def off_topic(state:AgentState):
    msg = AIMessage(content=(
            "I'm here to help with your shopping queries, "
            "but I’m not able to answer that particular question. "
            "Could you please ask something related to our products or services?"
        )

    )
    # Append response to state messages
    state["messages"] = state.get("messages", []) + [msg]

    return state