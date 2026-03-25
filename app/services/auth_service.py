from app.core.security import SecurityUtils

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code

class AuthService:
    def __init__(self, security: SecurityUtils = None):
        self.security = security or SecurityUtils()

    async def register_user(self, user_data):
        # 实际业务逻辑：密码哈希
        hashed_password = await self.security.get_password_hash(user_data.password)
        # 存入数据库逻辑 (占位)
        return {"username": user_data.username, "email": user_data.email}

    async def login_user(self, login_data):
        # 实际实现登录逻辑
        raise AuthError("Authentication logic not implemented", status_code=501)
