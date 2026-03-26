from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.models import ChatSession, ChatMessage
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., description="Unique session ID")

@router.post("/chat")
async def chat(request: Request, chat_req: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 获取或创建会话
        session = await db.get(ChatSession, chat_req.session_id)
        if not session:
            session = ChatSession(id=chat_req.session_id)
            db.add(session)
            await db.commit()
            
        # 记录用户消息
        user_msg = ChatMessage(session_id=session.id, role="human", content=chat_req.message)
        db.add(user_msg)
        
        # 调用 AI (此处保留原有 Graph 调用，或者替换为调用 LLM 的逻辑)
        graph = request.app.state.graph
        config = {"configurable": {"thread_id": session.id}}
        result = await graph.ainvoke({"messages": [chat_req.message]}, config=config)
        
        ai_response = result["messages"][-1]
        
        # 记录 AI 消息
        ai_msg = ChatMessage(session_id=session.id, role="ai", content=ai_response)
        db.add(ai_msg)
        await db.commit()
        
        return {"response": ai_response, "session_id": session.id}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
