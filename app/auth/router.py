from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import AuthToken
from .utils import create_jwt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(token: str, db: Session = Depends(get_db)):
    auth = db.query(AuthToken).filter(AuthToken.token == token).first()
    if not auth:
        raise HTTPException(status_code=403, detail="Token invalide")
    jwt_token = create_jwt({"sub": token})
    return {"access_token": jwt_token}
