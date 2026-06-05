from typing import Optional

from pydantic import BaseModel


class TacheCreate(BaseModel):
    demandeur_id: int
    categorie_id: Optional[int] = None
    titre: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    prix: float
    duree_estimee_min: Optional[int] = None


class AccepterTache(BaseModel):
    executant_id: int
