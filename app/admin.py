from fastapi import APIRouter, HTTPException
from app.models import AdminAuthRequest, StoredUser
from app.db import get_user_by_password, upsert_user, read_users
from app.settings import settings

router = APIRouter(prefix="/admin")

def check_admin_password(admin_password: str):
    if admin_password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Mot de passe admin incorrect")

@router.post("/add-password")
def add_password(request: AdminAuthRequest):
    check_admin_password(request.admin_password)

    if not request.password:
        raise HTTPException(status_code=400, detail="Mot de passe requis")

    existing = get_user_by_password(request.password)
    if existing:
        return {"message": "Utilisateur déjà existant"}

    new_user = StoredUser(password=request.password)
    upsert_user(new_user)
    return {"message": "Utilisateur ajouté"}

@router.post("/list")
def list_users(request: AdminAuthRequest):
    check_admin_password(request.admin_password)
    return read_users()
