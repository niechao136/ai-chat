from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService, AuthError
from app.core.database import get_db

router = APIRouter()

def get_auth_service():
    return AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db), auth: AuthService = Depends(get_auth_service)):
    return await auth.register_user(db, user)

@router.post("/login")
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db), auth: AuthService = Depends(get_auth_service)):
    result = await auth.login_user(db, login_data)
    # 可以在此处生成 Token，为了简化演示直接返回 user_id
    return {"message": "Login successful", "user_id": result["user_id"]}
