from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from pydantic import BaseModel, Field
from app.services.chat_graph import create_chat_graph
from app.core.database import get_db
from app.core.models import ChatSession, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
graph = create_chat_graph()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., description="Unique session ID")

@router.post("/chat")
async def chat(request: Request, chat_req: ChatRequest, user_id: int = Header(None), db: AsyncSession = Depends(get_db)):
    try:
        # 如果 user_id 存在，绑定到用户 ID，否则使用匿名 ID
        thread_id = f"user_{user_id}:{chat_req.session_id}" if user_id else f"anon:{chat_req.session_id}"
        
        # 数据库持久化逻辑：关联 session 和 user_id
        session = await db.execute(select(ChatSession).filter(ChatSession.id == thread_id))
        session = session.scalar_one_or_none()
        
        if not session:
            session = ChatSession(id=thread_id, user_id=user_id)
            db.add(session)
            await db.commit()
            
        # 记录用户消息
        db.add(ChatMessage(session_id=thread_id, role="human", content=chat_req.message))
        
        # 调用 AI (LangGraph)
        config = {"configurable": {"thread_id": thread_id}}
        result = await graph.ainvoke({"messages": [chat_req.message]}, config=config)
        
        ai_response = result["messages"][-1]
        
        # 记录 AI 消息
        db.add(ChatMessage(session_id=thread_id, role="ai", content=ai_response))
        await db.commit()
        
        return {"response": ai_response, "session_id": chat_req.session_id}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Chat processing failed")
