from app.core.database import db_cursor


def get_notifications(user_id):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute(
            """
            SELECT t.id,t.titre,t.statut,t.demandeur_id,t.executant_id,
                   t.date_acceptation,t.date_fin,
                   ud.prenom AS dem_prenom,ue.prenom AS exe_prenom
            FROM tache t
            LEFT JOIN utilisateur ud ON t.demandeur_id=ud.id
            LEFT JOIN utilisateur ue ON t.executant_id=ue.id
            WHERE (t.demandeur_id=%s OR t.executant_id=%s)
              AND t.statut IN ('acceptee','en_cours','terminee')
              AND (
                (t.statut='acceptee' AND t.date_acceptation >= NOW() - INTERVAL 5 MINUTE)
                OR (t.statut IN ('en_cours','terminee') AND t.date_fin >= NOW() - INTERVAL 5 MINUTE)
                OR (t.statut='en_cours' AND t.date_acceptation >= NOW() - INTERVAL 5 MINUTE)
              )
        """,
            (user_id, user_id),
        )
        rows = cur.fetchall()
        notifications = []
        for row in rows:
            if row["statut"] == "acceptee" and row["demandeur_id"] == user_id:
                notifications.append(
                    {
                        "type": "accepted",
                        "titre": row["titre"],
                        "msg": f"{row['exe_prenom']} a accepte votre mission \"{row['titre']}\" !",
                        "tache_id": row["id"],
                    }
                )
            elif row["statut"] == "terminee" and row["executant_id"] == user_id:
                notifications.append(
                    {
                        "type": "done",
                        "titre": row["titre"],
                        "msg": f"Mission \"{row['titre']}\" terminee - paiement en cours !",
                        "tache_id": row["id"],
                    }
                )
            elif row["statut"] == "en_cours" and row["demandeur_id"] == user_id:
                notifications.append(
                    {
                        "type": "started",
                        "titre": row["titre"],
                        "msg": f"{row['exe_prenom']} a demarre \"{row['titre']}\" !",
                        "tache_id": row["id"],
                    }
                )
        return {"notifications": notifications}
