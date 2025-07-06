from fastapi import APIRouter, HTTPException, Depends, Header
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Set

from app.models import LoginRequest, TokenResponse, UserUpdateRequest, StoredUser
from app.db import get_user_by_password, upsert_user
from app.settings import settings

router = APIRouter()

# Blacklist pour stocker les tokens invalidés
blacklisted_tokens: Set[str] = set()

def invalidate_token(token: str):
    """Ajoute un token à la blacklist pour l'invalider"""
    blacklisted_tokens.add(token)

def create_jwt_token(password: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": password,
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def verify_token(token: str) -> str:
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token invalidé")
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

def get_current_user(authorization: Optional[str] = Header(None)) -> StoredUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    token = authorization.split(" ")[1]
    password = verify_token(token)
    user = get_user_by_password(password)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

@router.get("/me", response_model=StoredUser)
def get_me(current_user: StoredUser = Depends(get_current_user)) -> StoredUser:
    return current_user

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = get_user_by_password(data.password)
    if not user:
        raise HTTPException(status_code=403, detail="Mot de passe invalide")
    token = create_jwt_token(data.password)
    return TokenResponse(access_token=token)

@router.post("/update")
def update_user(data: UserUpdateRequest, current_user: StoredUser = Depends(get_current_user)):
    updated_user = StoredUser(
        password=current_user.password,
        email=data.email if data.email is not None else current_user.email,
        infos=data.infos if data.infos is not None else current_user.infos
    )
    upsert_user(updated_user)
    return {"message": "Informations mises à jour"}
