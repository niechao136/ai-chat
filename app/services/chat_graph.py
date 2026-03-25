from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver 
from pydantic import Field

# 限制消息列表大小防止内存溢出 (简单的截断策略)
def reduce_messages(left: list[str], right: list[str]) -> list[str]:
    combined = left + right
    return combined[-20:]  # 仅保留最近 20 条

class AgentState(TypedDict):
    messages: Annotated[list[str], reduce_messages]

async def chat_node(state: AgentState):
    # 模拟简单的 echo
    last_message = state["messages"][-1]
    return {"messages": [f"Echo: {last_message}"]}

async def init_graph():
    graph = StateGraph(AgentState)
    graph.add_node("chat", chat_node)
    graph.set_entry_point("chat")
    graph.add_edge("chat", END)
    # 生产建议使用 Postgres/Redis，此处为了兼容性保留 MemorySaver
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
