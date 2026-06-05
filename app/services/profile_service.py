from fastapi import HTTPException

from app.core.database import db_cursor


def update_position(user_id, req):
    with db_cursor(dictionary=False) as (db, cur):
        cur.execute(
            "UPDATE utilisateur SET latitude=%s,longitude=%s WHERE id=%s",
            (req.latitude, req.longitude, user_id),
        )
        db.commit()
        return {"success": True}


def get_profile(user_id):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT id,nom,prenom,email,telephone,note_moyenne,nb_avis,date_inscription,est_verifie
            FROM utilisateur WHERE id=%s""",
            (user_id,),
        )
        user = cur.fetchone()
        if not user:
            raise HTTPException(404, "Utilisateur introuvable")

        cur.execute(
            """SELECT t.id,t.titre,t.prix,t.statut,t.statut_paiement,t.date_creation,
                   t.demandeur_id,t.executant_id,
                   ud.prenom AS dem_prenom,ud.nom AS dem_nom,
                   ue.prenom AS exe_prenom,ue.nom AS exe_nom,
                   c.nom AS cat_nom,
                   CASE WHEN t.demandeur_id=%s THEN 'demandeur' ELSE 'executant' END AS role,
                   (SELECT COUNT(*) FROM avis a WHERE a.tache_id=t.id AND a.auteur_id=%s) AS avis_deja_laisse
            FROM tache t
            LEFT JOIN utilisateur ud ON t.demandeur_id=ud.id
            LEFT JOIN utilisateur ue ON t.executant_id=ue.id
            LEFT JOIN categorie_tache c ON t.categorie_id=c.id
            WHERE t.demandeur_id=%s OR t.executant_id=%s
            ORDER BY t.date_creation DESC LIMIT 50""",
            (user_id, user_id, user_id, user_id),
        )
        missions = cur.fetchall()
        user["note_moyenne"] = float(user["note_moyenne"]) if user["note_moyenne"] else 0.0
        user["nb_avis"] = user["nb_avis"] or 0
        user["date_inscription"] = (
            user["date_inscription"].isoformat() if user["date_inscription"] else None
        )
        for mission in missions:
            mission["prix"] = float(mission["prix"])
            mission["avis_deja_laisse"] = bool(mission["avis_deja_laisse"])
            mission["date_creation"] = (
                mission["date_creation"].isoformat() if mission["date_creation"] else None
            )
        return {"utilisateur": user, "missions": missions}


def get_user_reviews(user_id):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT a.id,a.note,a.commentaire,a.date_creation,
                   u.prenom AS auteur_prenom,u.nom AS auteur_nom,t.titre AS tache_titre
            FROM avis a JOIN utilisateur u ON a.auteur_id=u.id JOIN tache t ON a.tache_id=t.id
            WHERE a.cible_id=%s ORDER BY a.date_creation DESC""",
            (user_id,),
        )
        reviews = cur.fetchall()
        for review in reviews:
            review["date_creation"] = (
                review["date_creation"].isoformat() if review["date_creation"] else None
            )
        return {"avis": reviews}


def get_wallet(user_id):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT COALESCE(SUM(tr.montant_executant),0) AS solde
            FROM transaction tr JOIN tache t ON tr.tache_id=t.id
            WHERE t.executant_id=%s AND tr.statut='versee'""",
            (user_id,),
        )
        solde = float(cur.fetchone()["solde"])
        cur.execute(
            """SELECT COALESCE(SUM(tr.montant_executant),0) AS att
            FROM transaction tr JOIN tache t ON tr.tache_id=t.id
            WHERE t.executant_id=%s AND tr.statut='en_attente'""",
            (user_id,),
        )
        attente = float(cur.fetchone()["att"])
        cur.execute(
            """SELECT COALESCE(SUM(tr.montant_total),0) AS dep
            FROM transaction tr JOIN tache t ON tr.tache_id=t.id
            WHERE t.demandeur_id=%s AND tr.statut='versee'""",
            (user_id,),
        )
        depense = float(cur.fetchone()["dep"])
        cur.execute(
            """SELECT tr.*,t.titre,t.demandeur_id,t.executant_id,
                   CASE WHEN t.executant_id=%s THEN 'credit' ELSE 'debit' END AS sens
            FROM transaction tr JOIN tache t ON tr.tache_id=t.id
            WHERE t.demandeur_id=%s OR t.executant_id=%s
            ORDER BY tr.date_transaction DESC LIMIT 10""",
            (user_id, user_id, user_id),
        )
        rows = cur.fetchall()
        for row in rows:
            row["montant_total"] = float(row["montant_total"])
            row["montant_executant"] = float(row["montant_executant"])
            row["commission_plateforme"] = float(row["commission_plateforme"])
            row["date_transaction"] = (
                row["date_transaction"].isoformat() if row["date_transaction"] else None
            )
        return {
            "solde": round(solde, 2),
            "en_attente": round(attente, 2),
            "depense": round(depense, 2),
            "transactions": rows,
        }
