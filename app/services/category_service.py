from app.core.database import db_cursor


def list_categories():
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute("SELECT * FROM categorie_tache ORDER BY nom")
        categories = cur.fetchall()
        for category in categories:
            category["prix_suggere"] = float(category["prix_suggere"])
        return {"categories": categories}
