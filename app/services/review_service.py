from fastapi import HTTPException

from app.core.database import db_cursor


def post_review(review):
    if not 1 <= review.note <= 5:
        raise HTTPException(400, "Note entre 1 et 5")
    if review.auteur_id == review.cible_id:
        raise HTTPException(400, "Impossible de se noter soi-meme")

    with db_cursor(dictionary=True) as (db, cur):
        cur.execute(
            "SELECT id FROM avis WHERE tache_id=%s AND auteur_id=%s",
            (review.tache_id, review.auteur_id),
        )
        if cur.fetchone():
            raise HTTPException(400, "Avis deja publie pour cette mission")

        cur.execute(
            "INSERT INTO avis (tache_id,auteur_id,cible_id,note,commentaire) VALUES(%s,%s,%s,%s,%s)",
            (
                review.tache_id,
                review.auteur_id,
                review.cible_id,
                review.note,
                review.commentaire,
            ),
        )
        cur.execute(
            """UPDATE utilisateur
            SET note_moyenne=(SELECT AVG(note) FROM avis WHERE cible_id=%s),
                nb_avis=(SELECT COUNT(*) FROM avis WHERE cible_id=%s)
            WHERE id=%s""",
            (review.cible_id, review.cible_id, review.cible_id),
        )
        db.commit()
        return {"success": True, "message": "Avis publie, merci !"}
