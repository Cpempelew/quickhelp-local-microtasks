from fastapi import HTTPException

from app.core.database import db_cursor
from app.utils.geo import distance_km


def list_tasks(user_lat=48.8566, user_lon=2.3522, rayon_km=10.0):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT t.*,u.prenom AS dem_prenom,u.nom AS dem_nom,
                   u.note_moyenne AS dem_note,c.nom AS cat_nom,c.duree_estimee_min AS duree
            FROM tache t JOIN utilisateur u ON t.demandeur_id=u.id
            LEFT JOIN categorie_tache c ON t.categorie_id=c.id
            WHERE t.statut='publiee'"""
        )
        tasks = []
        for task in cur.fetchall():
            distance = distance_km(
                user_lat,
                user_lon,
                float(task["latitude"]),
                float(task["longitude"]),
            )
            if distance <= rayon_km:
                task["distance_km"] = round(distance, 2)
                task["prix"] = float(task["prix"])
                task["latitude"] = float(task["latitude"])
                task["longitude"] = float(task["longitude"])
                task["dem_note"] = float(task["dem_note"]) if task["dem_note"] else 0.0
                task["date_creation"] = (
                    task["date_creation"].isoformat() if task["date_creation"] else None
                )
                tasks.append(task)
        tasks.sort(key=lambda item: item["distance_km"])
        return {"taches": tasks, "total": len(tasks)}


def create_task(task):
    with db_cursor(dictionary=False) as (db, cur):
        cur.execute(
            """INSERT INTO tache
            (demandeur_id,categorie_id,titre,description,latitude,longitude,prix)
            VALUES(%s,%s,%s,%s,%s,%s,%s)""",
            (
                task.demandeur_id,
                task.categorie_id,
                task.titre,
                task.description,
                task.latitude,
                task.longitude,
                task.prix,
            ),
        )
        db.commit()
        return {"success": True, "tache_id": cur.lastrowid, "message": "Mission publiee !"}


def accept_task(task_id, req):
    with db_cursor(dictionary=True) as (db, cur):
        cur.execute("SELECT * FROM tache WHERE id=%s AND statut='publiee'", (task_id,))
        task = cur.fetchone()
        if not task:
            raise HTTPException(404, "Mission introuvable ou deja prise")
        if task["demandeur_id"] == req.executant_id:
            raise HTTPException(400, "Vous ne pouvez pas accepter votre propre mission")

        cur.execute(
            "UPDATE tache SET executant_id=%s,statut='acceptee',date_acceptation=NOW() WHERE id=%s",
            (req.executant_id, task_id),
        )
        commission = round(float(task["prix"]) * 0.10, 2)
        cur.execute(
            """INSERT INTO transaction (tache_id,montant_total,montant_executant,commission_plateforme)
            VALUES(%s,%s,%s,%s)""",
            (
                task_id,
                float(task["prix"]),
                round(float(task["prix"]) - commission, 2),
                commission,
            ),
        )
        db.commit()
        return {"success": True, "message": "Mission acceptee ! Bonne chance"}


def start_task(task_id):
    with db_cursor(dictionary=True) as (db, cur):
        cur.execute("SELECT statut FROM tache WHERE id=%s", (task_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, "Mission introuvable")
        if row["statut"] != "acceptee":
            raise HTTPException(400, "La mission doit etre acceptee d'abord")

        cur.execute("UPDATE tache SET statut='en_cours' WHERE id=%s", (task_id,))
        db.commit()
        return {"success": True, "message": "Mission demarree !"}


def finish_task(task_id):
    with db_cursor(dictionary=False) as (db, cur):
        cur.execute("UPDATE tache SET statut='terminee',date_fin=NOW() WHERE id=%s", (task_id,))
        cur.execute("UPDATE transaction SET statut='versee' WHERE tache_id=%s", (task_id,))
        db.commit()
        return {"success": True, "message": "Mission terminee ! Paiement libere"}


def validate_payment(task_id):
    with db_cursor(dictionary=False) as (db, cur):
        cur.execute(
            "UPDATE transaction SET statut='validee' WHERE tache_id=%s AND statut='en_attente'",
            (task_id,),
        )
        cur.execute("UPDATE tache SET statut_paiement='valide' WHERE id=%s", (task_id,))
        db.commit()
        return {"success": True, "message": "Paiement valide"}
