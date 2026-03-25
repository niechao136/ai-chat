from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService, AuthError

router = APIRouter()

def get_auth_service():
    return AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, auth: AuthService = Depends(get_auth_service)):
    return await auth.register_user(user)

@router.post("/login")
async def login(login_data: UserLogin, auth: AuthService = Depends(get_auth_service)):
    try:
        return await auth.login_user(login_data)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=e.message)
