import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCbhuyl9ZrTuib4EnF7mtAZwx3N1OB6Nvw"

from langchain_core.messages import HumanMessage

from src.schema.agent_schemes import AgentState
from src.agents.init_agent import agent
# --- Test ---
prompt_text = "what is the office location " 

# Create a valid initial state with all required keys
initial_state: AgentState = {
    "messages": [HumanMessage(content=prompt_text)],
    "user_id": "bff558d9-4329-446b-ada4-95722036a94e" 
}

import asyncio

# Invoke the graph asynchronously
response = asyncio.run(app.ainvoke(initial_state))
print(response)



