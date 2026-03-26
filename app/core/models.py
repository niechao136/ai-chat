from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, index=True) # session_id (可以是匿名id)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # 关联登录用户
    created_at = Column(DateTime, default=func.now())
    
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    role = Column(String) # human / ai
    content = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    session = relationship("ChatSession", back_populates="messages")
