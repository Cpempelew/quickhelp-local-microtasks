from app.core.config import ADMIN_EMAIL
from app.core.database import db_cursor


def get_stats():
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute("SELECT COUNT(*) as c FROM utilisateur WHERE email != %s", (ADMIN_EMAIL,))
        nb_users = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM tache")
        nb_taches = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM tache WHERE statut='publiee'")
        nb_dispo = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM tache WHERE statut='terminee'")
        nb_done = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) as c FROM transaction")
        nb_tx = cur.fetchone()["c"]
        cur.execute("SELECT COALESCE(SUM(montant_total),0) as s FROM transaction WHERE statut='versee'")
        volume = float(cur.fetchone()["s"])
        cur.execute(
            "SELECT COALESCE(SUM(commission_plateforme),0) as s FROM transaction WHERE statut='versee'"
        )
        commissions = float(cur.fetchone()["s"])
        cur.execute("SELECT COUNT(*) as c FROM avis")
        nb_avis = cur.fetchone()["c"]
        cur.execute("SELECT COALESCE(AVG(note),0) as a FROM avis")
        avg_note = float(cur.fetchone()["a"])
        return {
            "nb_users": nb_users,
            "nb_taches": nb_taches,
            "nb_dispo": nb_dispo,
            "nb_done": nb_done,
            "nb_transactions": nb_tx,
            "volume_total": round(volume, 2),
            "commissions": round(commissions, 2),
            "nb_avis": nb_avis,
            "note_moyenne": round(avg_note, 2),
        }


def list_missions():
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT t.*,ud.prenom AS dem_prenom,ud.nom AS dem_nom,
                   ue.prenom AS exe_prenom,ue.nom AS exe_nom,c.nom AS cat_nom
            FROM tache t
            LEFT JOIN utilisateur ud ON t.demandeur_id=ud.id
            LEFT JOIN utilisateur ue ON t.executant_id=ue.id
            LEFT JOIN categorie_tache c ON t.categorie_id=c.id
            ORDER BY t.date_creation DESC"""
        )
        rows = cur.fetchall()
        for row in rows:
            row["prix"] = float(row["prix"])
            row["date_creation"] = row["date_creation"].isoformat() if row["date_creation"] else None
        return {"missions": rows, "total": len(rows)}


def list_users():
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT u.id,u.nom,u.prenom,u.email,u.telephone,
                   u.note_moyenne,u.nb_avis,u.est_verifie,u.date_inscription,
                   COUNT(DISTINCT t.id) AS nb_missions
            FROM utilisateur u LEFT JOIN tache t ON (t.demandeur_id=u.id OR t.executant_id=u.id)
            WHERE u.email != %s
            GROUP BY u.id ORDER BY u.date_inscription DESC""",
            (ADMIN_EMAIL,),
        )
        rows = cur.fetchall()
        for row in rows:
            row["note_moyenne"] = float(row["note_moyenne"]) if row["note_moyenne"] else 0.0
            row["date_inscription"] = (
                row["date_inscription"].isoformat() if row["date_inscription"] else None
            )
        return {"utilisateurs": rows, "total": len(rows)}


def list_transactions():
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """SELECT tr.*,t.titre,ud.prenom AS dem_prenom,ue.prenom AS exe_prenom
            FROM transaction tr JOIN tache t ON tr.tache_id=t.id
            LEFT JOIN utilisateur ud ON t.demandeur_id=ud.id
            LEFT JOIN utilisateur ue ON t.executant_id=ue.id
            ORDER BY tr.date_transaction DESC"""
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
            "transactions": rows,
            "total": len(rows),
            "total_commissions": round(sum(row["commission_plateforme"] for row in rows), 2),
        }
