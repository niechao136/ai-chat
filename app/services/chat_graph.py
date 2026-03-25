from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver 

class AgentState(TypedDict):
    messages: Annotated[list[str], operator.add]

async def chat_node(state: AgentState):
    # 模拟简单的 echo
    last_message = state["messages"][-1]
    return {"messages": [f"Echo: {last_message}"]}

async def init_graph():
    # 使用现代版本 StateGraph
    graph = StateGraph(AgentState)
    graph.add_node("chat", chat_node)
    graph.set_entry_point("chat")
    graph.add_edge("chat", END)
    
    # 生产建议使用 Postgres/Redis，此处为了兼容性保留 MemorySaver
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
