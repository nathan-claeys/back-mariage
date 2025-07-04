import json
from typing import List, Optional
from pathlib import Path
from app.models import StoredUser

DB_PATH = Path("data/users.json")

# Lire tous les utilisateurs du fichier
def read_users() -> List[StoredUser]:
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [StoredUser(**user) for user in data.get("users", [])]

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
