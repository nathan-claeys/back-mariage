from fastapi import APIRouter, HTTPException
from app.models import AdminAuthRequest, StoredUser, StoredEvent, AdminEventRequest
from app.db import get_user_by_password, upsert_user, read_users, upsert_event, remove_user_by_password, remove_event_by_name, read_events


from app.settings import settings

router = APIRouter(prefix="/admin")

def check_admin_password(admin_password: str):
    if admin_password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Mot de passe admin incorrect")
    
@router.post("/is-admin", response_model=bool)
def is_admin(request: AdminAuthRequest):
    """
    Vérifie si le mot de passe admin est correct.
    Retourne True si c'est le cas, sinon lève une exception HTTP 403.
    """
    check_admin_password(request.admin_password)
    return True

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

@router.delete("/remove-user")
def remove_user(request: AdminAuthRequest):
    check_admin_password(request.admin_password)

    if not request.password:
        raise HTTPException(status_code=400, detail="Mot de passe requis")
    
    removed = remove_user_by_password(request.password)
    if not removed:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur supprimé"}

@router.post("/list")
def list_users(request: AdminAuthRequest):
    check_admin_password(request.admin_password)
    return read_users()

@router.post("/add-event")
def add_event(request: AdminEventRequest):
    check_admin_password(request.admin_password)
    event = StoredEvent(name=request.name, date=request.date, link=request.link)
    upsert_event(event)
    return {"message": "Evénement ajouté"}

@router.delete("/remove-event/{event_name}")
def remove_event(request: AdminAuthRequest, event_name: str):
    check_admin_password(request.admin_password)
    removed = remove_event_by_name(event_name)
    if not removed:
        raise HTTPException(status_code=404, detail="Evénement non trouvé")
    return {"message": "Evénement supprimé"}

@router.post("/list-events")
def list_events(request: AdminAuthRequest):
    check_admin_password(request.admin_password)
    return read_events()
    