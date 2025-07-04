from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

# Représente un utilisateur dans la base JSON
class StoredUser(BaseModel):
    password: str
    email: Optional[EmailStr] = None
    infos: Optional[Dict[str, str]] = {}

# Requête de login
class LoginRequest(BaseModel):
    password: str

# Réponse contenant un token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Requête de mise à jour du profil utilisateur
class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    infos: Optional[Dict[str, str]] = {}

# Requête pour les routes admin
class AdminAuthRequest(BaseModel):
    admin_password: str
    password: Optional[str] = None

class AdminEventRequest(BaseModel):
    admin_password: str
    name: str
    date: str
    link: Optional[str] = None  

class StoredEvent(BaseModel):
    name : str
    date : str
    link : Optional[str]
