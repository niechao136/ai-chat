from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.core.config import settings

# 配置 OpenAI 客户端以使用 Gemini API
if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in settings")

llm = ChatOpenAI(
    model="gemini-3-flash-preview",
    api_key=settings.GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class AgentState(TypedDict):
    messages: Annotated[list[str], operator.add]

async def chat_node(state: AgentState):
    # 调用 Gemini
    response = await llm.ainvoke([HumanMessage(content=state["messages"][-1])])
    return {"messages": [response.content]}

def create_chat_graph():
    graph = StateGraph(AgentState)
    graph.add_node("chat", chat_node)
    graph.set_entry_point("chat")
    graph.add_edge("chat", END)
    
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)

async def init_graph():
    return create_chat_graph()
