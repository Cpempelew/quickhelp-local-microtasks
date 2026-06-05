from fastapi import APIRouter

from app.schemas.tasks import AccepterTache, TacheCreate
from app.services.task_service import (
    accept_task,
    create_task,
    finish_task,
    list_tasks,
    start_task,
    validate_payment,
)

router = APIRouter(tags=["taches"])


@router.get("/taches")
def get_taches(user_lat: float = 48.8566, user_lon: float = 2.3522, rayon_km: float = 10.0):
    return list_tasks(user_lat, user_lon, rayon_km)


@router.post("/taches")
def creer_tache(task: TacheCreate):
    return create_task(task)


@router.put("/taches/{task_id}/accepter")
def accepter(task_id: int, req: AccepterTache):
    return accept_task(task_id, req)


@router.put("/taches/{task_id}/demarrer")
def demarrer(task_id: int):
    return start_task(task_id)


@router.put("/taches/{task_id}/terminer")
def terminer(task_id: int):
    return finish_task(task_id)


@router.put("/taches/{task_id}/payer")
def valider_paiement(task_id: int):
    return validate_payment(task_id)
