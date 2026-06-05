from typing import Optional

from pydantic import BaseModel


class AvisCreate(BaseModel):
    tache_id: int
    auteur_id: int
    cible_id: int
    note: int
    commentaire: Optional[str] = None
