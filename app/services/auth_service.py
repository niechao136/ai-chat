from app.core.security import SecurityUtils

# 定义业务异常
class AuthError(Exception):
    def __init__(self, message: str):
        self.message = message

class AuthService:
    def __init__(self, security: SecurityUtils = None):
        self.security = security or SecurityUtils()

    async def register_user(self, user_data):
        # 实际业务逻辑
        return {"username": user_data.username}

    async def login_user(self, login_data):
        # 实际业务逻辑，抛出自定义异常
        raise AuthError("Authentication logic not implemented")
