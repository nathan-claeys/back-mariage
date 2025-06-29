from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from ..settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pwd):
    return pwd_context.hash(pwd)

def verify_password(pwd, hashed):
    return pwd_context.verify(pwd, hashed)

def create_jwt(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
