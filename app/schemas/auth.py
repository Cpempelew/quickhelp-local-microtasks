from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    mot_de_passe: str


class RegisterRequest(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    telephone: Optional[str] = None
    latitude: Optional[float] = 48.8566
    longitude: Optional[float] = 2.3522
