from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.schema.agent_schemes import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def rewriter_node(state:AgentState):
    state["topic"] = ""
    state["refine_question"] = ""
    state["order_type"] = ""

    current_question = state.get('messages', [])[-1]

    if "messages" not in state or state["messages"] is None:
        state["messages"] = []
    if current_question not in state["messages"]:
        state["messages"].append(HumanMessage(content=current_question.content)) # type: ignore

    if len(state["messages"]) > 1:
        question = current_question.content # type: ignore
        conversations = state['messages'][:-1]
        conversations.extend(
            [
                SystemMessage(content="""
                    You are a helpful assistant. 
                    Rephrase the user's query clearly and concisely without changing its meaning.
                    Extract all relevant details like product item details where needed
                    Focus on the last user message while considering prior conversation context.
                    Return a complete, structured, and concise refined query.
                """),
                HumanMessage(content=question)
            ]
        )
        rephrase_prompt = ChatPromptTemplate.from_messages(conversations)
        response = await llm.ainvoke(rephrase_prompt.format())
        state["refine_question"] = str(response.content)
    else: 
        state["refine_question"] = str(current_question.content) # type: ignore
    return state
