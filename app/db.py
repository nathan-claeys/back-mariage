import json
from typing import List, Optional
from pathlib import Path
from app.models import StoredUser, StoredEvent

DB_PATH = Path("data/users.json")

DB_EVENT_PATH = Path("data/events.json")


# Lire tous les utilisateurs du fichier
def read_users() -> List[StoredUser]:
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [StoredUser(**user) for user in data.get("users", [])]

# Lire tous les events du fichier
def read_events() -> List[StoredEvent]:
    if not DB_EVENT_PATH.exists():
        return []
    with open(DB_EVENT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [StoredEvent(**event) for event in data.get("events", [])]

# Trouver un utilisateur par son mot de passe
def get_user_by_password(password: str) -> Optional[StoredUser]:
    users = read_users()
    for user in users:
        if user.password == password:
            return user
    return None

# Ajouter ou mettre à jour un utilisateur
def upsert_user(new_user: StoredUser) -> None:
    users = read_users()
    for i, user in enumerate(users):
        if user.password == new_user.password:
            users[i] = new_user
            break
    else:
        users.append(new_user)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump({"users": [u.dict() for u in users]}, f, indent=2)

# Retirer un utilisateur par son mot de passe
def remove_user_by_password(password: str) -> bool:
    users = read_users()
    for i, user in enumerate(users):
        if user.password == password:
            del users[i]
            break
    else:
        return False  # No user with the given password was found
    
    with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": [u.model_dump() for u in users]}, f, indent=2)
            return True  # User was found and removed
    

# Ajouter ou mettez à jour un événement
def upsert_event(storedEvent: StoredEvent) -> None:
    events = read_events()
    for i, event in enumerate(events):
        if event.name == storedEvent.name:
            events[i] = storedEvent
            break
            
    else:
        events.append(storedEvent)
       
    with open(DB_EVENT_PATH, "w", encoding="utf-8") as f:
            json.dump({"events": [e.model_dump() for e in events]}, f, indent=2)


# Retirer un événement par son nom
def remove_event_by_name(name: str) -> bool:
    events = read_events()
    for i, event in enumerate(events):
        if event.name == name:
            del events[i]
            break
    else:
        return False   # No event with the given name was found
    
    with open(DB_EVENT_PATH, "w", encoding="utf-8") as f:
        json.dump({"events": [e.model_dump() for e in events]}, f, indent=2)
        return True   # Event was found and removed
    

# Trouver un evénement par son nom
def get_event_by_name(name: str) -> Optional[StoredEvent]:
    events = read_events()
    for event in events:
        if event.name == name:
            return event
    return None


