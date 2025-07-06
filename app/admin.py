from fastapi import APIRouter, HTTPException, Depends, Header
from app.models import AdminAuthRequest, StoredUser, StoredEvent, AdminEventRequest, TokenResponse
from app.db import get_user_by_password, upsert_user, read_users, upsert_event, remove_user_by_password, remove_event_by_name, read_events
from app.auth import get_current_user, create_jwt_token, invalidate_token
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from app.settings import settings

router = APIRouter(prefix="/admin")

def create_expired_token(password: str) -> str:
    """Crée un token déjà expiré pour forcer la déconnexion"""
    expire = datetime.utcnow() - timedelta(minutes=1)  # Token expiré il y a 1 minute
    payload = {
        "sub": password,
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def check_admin_password(admin_password: str):
    if admin_password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Mot de passe admin incorrect")
    
@router.post("/is-admin", response_model=TokenResponse)
def is_admin(request: AdminAuthRequest, current_user: StoredUser = Depends(get_current_user), authorization: Optional[str] = Header(None)):
    """
    Vérifie si le mot de passe admin est correct.
    Si incorrect, invalide le token actuel pour forcer la déconnexion.
    """
    try:
        check_admin_password(request.admin_password)
        # Si le mot de passe est correct, retourner un nouveau token valide
        new_token = create_jwt_token(current_user.password)
        return TokenResponse(access_token=new_token)
    except HTTPException as e:
        if e.status_code == 403:
            # Invalider le token actuel
            if authorization and authorization.startswith("Bearer "):
                current_token = authorization.split(" ")[1]
                invalidate_token(current_token)
            raise HTTPException(status_code=403, detail="Mot de passe admin incorrect")
        raise

@router.post("/add-password")
def add_password(request: AdminAuthRequest, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)

    if not request.password:
        raise HTTPException(status_code=400, detail="Mot de passe requis")

    existing = get_user_by_password(request.password)
    if existing:
        return {"message": "Utilisateur déjà existant"}

    new_user = StoredUser(password=request.password)
    upsert_user(new_user)
    return {"message": "Utilisateur ajouté"}

@router.delete("/remove-user")
def remove_user(request: AdminAuthRequest, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)

    if not request.password:
        raise HTTPException(status_code=400, detail="Mot de passe requis")
    
    removed = remove_user_by_password(request.password)
    if not removed:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur supprimé"}

@router.post("/list")
def list_users(request: AdminAuthRequest, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)
    return read_users()

@router.post("/add-event")
def add_event(request: AdminEventRequest, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)
    event = StoredEvent(name=request.name, date=request.date, link=request.link)
    upsert_event(event)
    return {"message": "Evénement ajouté"}

@router.delete("/remove-event/{event_name}")
def remove_event(request: AdminAuthRequest, event_name: str, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)
    removed = remove_event_by_name(event_name)
    if not removed:
        raise HTTPException(status_code=404, detail="Evénement non trouvé")
    return {"message": "Evénement supprimé"}

@router.post("/list-events")
def list_events(request: AdminAuthRequest, current_user: StoredUser = Depends(get_current_user)):
    check_admin_password(request.admin_password)
    return read_events()
    return read_events()
