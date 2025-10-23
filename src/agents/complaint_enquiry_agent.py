from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.utils.sample_docx import documents

from src.schema.agent_schemes import AgentState
from src.services.routers_service import route_handler

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


embedding_func = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

db = Chroma.from_documents(documents, embedding_func)
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 2})

async def complaint(state: AgentState):
    question = state.get("refine_question", "")
    user_id = state.get("user_id", "")

    task_prompt = f"""
        You are a customer support agent for Zion Mart.

        User Complaint: {question}
        User ID: {user_id}

        Instructions:
        1. Identify the most relevant department:
            - Sales → wrong item, order errors, or price issues.
            - Logistics → delivery delays, damaged, or missing goods.
            - Support → website/app issues, technical errors, or general queries.
            - Finance → payment failures, refunds, or billing problems.
        2. Use 'get_department' to determine the correct department.
        3. Use 'create_ticket' to log the complaint and assign it to the chosen department.
        4. Return a confirmation message that includes:
            - The assigned department
            - The generated complaint (ticket) ID
        5. If unsure, default to the Support department.
    """
    return await route_handler(state, task_prompt)


def formate_doc(docx):
    return "\n".join(doc.page_content for doc in docx)

async def enquiry(state: AgentState):
    question = state.get("refine_question", "")

    if retriever is None:
        raise ValueError("Retriever not found in state")

    context_docs = await retriever.ainvoke(str(question))
    context = formate_doc(context_docs)

    # Prepare prompt
    prompt_temp = f"""
        Use the following context to answer the user's question. 
        Do not use any external knowledge; rely only on the information provided in the context:

        Question: {question}
        Context: {context}
    """
    prompt = ChatPromptTemplate.from_template(prompt_temp)

    # Invoke LLM
    response = await llm.ainvoke(prompt.format())

    # Append response to state messages
    state["messages"] = state.get("messages", []) + [response]

    return state


