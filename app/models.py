from sqlalchemy import Column, Integer, String
from .db import Base

class AuthToken(Base):
    __tablename__ = "auth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(128), unique=True)
    email = Column(String(256), nullable=True)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String(256))
