from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from app.auth import verify_token
from app.models import StoredEvent
from app.db import get_event_by_name

router = APIRouter(prefix="/events")

@router.get("/{name}", response_model=StoredEvent)
def get_event(name: str, authorization: Optional[str] = Header(None)) -> StoredEvent: 
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    token = authorization.split(" ")[1]
    verify_token(token)
    event = get_event_by_name(name)
    if not event:
        raise HTTPException(status_code=404, detail="Evenement non trouvé")
    return event



