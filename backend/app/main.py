from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow requests from the Flask frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:5000"],  # Flask frontend 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.8,
    api_key='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',  
)

workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": response}

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app_compiled = workflow.compile(checkpointer=memory)

class MessageInput(BaseModel):
    messages: str
    thread_id: str = 'default_thread'  # Optional thread ID

@app.post("/chat")
async def chat(input_data: MessageInput):
    input_messages = input_data.messages
    config = {"configurable": {"thread_id": input_data.thread_id}}

    output = app_compiled.invoke({"messages": input_messages}, config)
    response_message = output["messages"][-1].content  # Assuming content is the response

    return {"response": response_message}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
