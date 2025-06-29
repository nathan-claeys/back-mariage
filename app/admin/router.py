from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import AuthToken
from ..settings import settings
from ..auth.utils import hash_password

router = APIRouter(prefix="/admin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_admin(password: str):
    if password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Unauthorized")

@router.post("/add-token")
def add_token(token: str, admin_pwd: str, db: Session = Depends(get_db)):
    is_admin(admin_pwd)
    db.add(AuthToken(token=token))
    db.commit()
    return {"message": "Token ajouté"}

@router.get("/list")
def list_tokens(admin_pwd: str, db: Session = Depends(get_db)):
    is_admin(admin_pwd)
    return db.query(AuthToken).all()

@router.delete("/delete")
def delete_token(token: str, admin_pwd: str, db: Session = Depends(get_db)):
    is_admin(admin_pwd)
    db.query(AuthToken).filter(AuthToken.token == token).delete()
    db.commit()
    return {"message": "Token supprimé"}
