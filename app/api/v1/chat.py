from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., description="Unique session ID for conversation context")

# 模拟当前用户获取逻辑
def get_current_user_id():
    return "default_user_id"

@router.post("/chat")
async def chat(request: Request, chat_req: ChatRequest, user_id: str = Depends(get_current_user_id)):
    # 从 app.state 获取 graph 实例
    graph = request.app.state.graph
    
    try:
        # 使用 user_id + session_id 构造全局唯一的 thread_id，防止越权
        thread_id = f"{user_id}:{chat_req.session_id}"
        config = {"configurable": {"thread_id": thread_id}}
        
        # 实际生产环境：建议增加对 thread_id 的权限验证
        
        result = await graph.ainvoke({"messages": [chat_req.message]}, config=config)
        
        if not result or "messages" not in result or not result["messages"]:
            raise ValueError("No response generated")
            
        return {"response": result["messages"][-1], "session_id": chat_req.session_id}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        # 区分不同类型的错误，生产建议使用自定义异常类
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An internal error occurred during chat processing."
        )
