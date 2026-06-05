import bcrypt
from fastapi import HTTPException

from app.core.database import db_cursor
from app.services.user_service import user_short


def login_user(req):
    with db_cursor(dictionary=True) as (_, cur):
        cur.execute("SELECT * FROM utilisateur WHERE email=%s", (req.email,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(401, "Email introuvable")
        if not bcrypt.checkpw(req.mot_de_passe.encode(), user["mot_de_passe_hash"].encode()):
            raise HTTPException(401, "Mot de passe incorrect")
        return {
            "success": True,
            "message": f"Bienvenue {user['prenom']} !",
            "utilisateur": user_short(user),
        }


def register_user(req):
    with db_cursor(dictionary=True) as (db, cur):
        cur.execute("SELECT id FROM utilisateur WHERE email=%s", (req.email,))
        if cur.fetchone():
            raise HTTPException(400, "Email deja utilise")

        password_hash = bcrypt.hashpw(req.mot_de_passe.encode(), bcrypt.gensalt()).decode()
        cur.execute(
            """INSERT INTO utilisateur
            (nom,prenom,email,mot_de_passe_hash,telephone,latitude,longitude,note_moyenne,nb_avis,est_verifie)
            VALUES(%s,%s,%s,%s,%s,%s,%s,0,0,1)""",
            (
                req.nom,
                req.prenom,
                req.email,
                password_hash,
                req.telephone,
                req.latitude,
                req.longitude,
            ),
        )
        db.commit()
        return {"success": True, "message": f"Compte cree ! Bienvenue {req.prenom} !"}
