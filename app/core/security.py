from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityUtils:
    async def get_password_hash(self, password: str):
        return await run_in_threadpool(pwd_context.hash, password)

    async def verify_password(self, plain_password: str, hashed_password: str):
        return await run_in_threadpool(pwd_context.verify, plain_password, hashed_password)
