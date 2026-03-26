from app.core.security import SecurityUtils
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import User

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code

class AuthService:
    def __init__(self, security: SecurityUtils = None):
        self.security = security or SecurityUtils()

    async def register_user(self, db: AsyncSession, user_data):
        # 检查用户名是否已存在
        result = await db.execute(select(User).filter(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise AuthError("Username already exists", status_code=400)
        
        hashed_password = await self.security.get_password_hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"username": new_user.username, "email": new_user.email}

    async def login_user(self, db: AsyncSession, login_data):
        result = await db.execute(select(User).filter(User.username == login_data.username))
        user = result.scalar_one_or_none()
        if not user or not await self.security.verify_password(login_data.password, user.hashed_password):
            raise AuthError("Invalid username or password")
        return {"username": user.username}
