import bcrypt

from app.core.config import ADMIN_EMAIL, ADMIN_PASSWORD
from app.core.database import db_cursor


def seed_database():
    try:
        with db_cursor(dictionary=True) as (db, cur):
            seed_categories(db, cur)
            seed_users(db, cur)
            seed_tasks(db, cur)
            seed_admin(db, cur)
        print("QuickHelp pret - http://localhost:8000")
    except Exception as exc:
        print(f"Erreur demarrage : {exc}")


def seed_categories(db, cur):
    cur.execute("SELECT COUNT(*) as c FROM categorie_tache")
    if cur.fetchone()["c"] != 0:
        return
    cur.execute(
        """INSERT INTO categorie_tache (nom,description,prix_suggere,duree_estimee_min) VALUES
        ('Courses alimentaires','Aller chercher des courses',8.00,30),
        ('Sortir les poubelles','Descendre/rentrer les poubelles',3.00,10),
        ('Aide informatique','Aide PC, smartphone, demarches',10.00,45),
        ('Porter des colis','Monter ou deplacer des colis',7.00,20),
        ('Arroser les plantes','Arroser plantes voisin absent',4.00,15),
        ('Accompagnement','Accompagner une personne a pied',6.00,60),
        ('Montage de meuble','Monter meuble type IKEA',12.00,90),
        ('Garde de courrier','Recuperer courrier pendant absence',3.00,10),
        ('Aide aux devoirs','Aide scolaire, revisions',15.00,60),
        ('Jardinage','Tondre, desherber, tailler',10.00,60)"""
    )
    db.commit()
    print("Categories creees")


def seed_users(db, cur):
    cur.execute("SELECT COUNT(*) as c FROM utilisateur")
    if cur.fetchone()["c"] != 0:
        return
    password_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()
    users = [
        ("Martin", "Sophie", "sophie.martin@email.fr", "0812345678", 48.8566, 2.3522, 4.8, 12, True),
        ("Dubois", "Lucas", "lucas.dubois@email.fr", "0823456789", 48.8600, 2.3488, 4.5, 8, True),
        ("Bernard", "Marie", "marie.bernard@email.fr", "0334567890", 48.8534, 2.3499, 4.9, 5, True),
        ("Leroy", "Paul", "paul.leroy@email.fr", "0245678901", 48.8580, 2.3600, 4.2, 3, False),
        ("Moreau", "Camille", "camille.moreau@email.fr", "0856789012", 48.8550, 2.3450, 0.0, 0, True),
        ("Petit", "Antoine", "antoine.petit@email.fr", "0267890123", 48.8520, 2.3560, 4.6, 6, True),
    ]
    for user in users:
        cur.execute(
            """INSERT INTO utilisateur
            (nom,prenom,email,mot_de_passe_hash,telephone,latitude,longitude,note_moyenne,nb_avis,est_verifie)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                user[0],
                user[1],
                user[2],
                password_hash,
                user[3],
                user[4],
                user[5],
                user[6],
                user[7],
                user[8],
            ),
        )
    db.commit()
    print("Utilisateurs crees - mdp: password123")


def seed_tasks(db, cur):
    cur.execute("SELECT COUNT(*) as c FROM tache")
    if cur.fetchone()["c"] != 0:
        return
    cur.execute("SELECT id FROM utilisateur ORDER BY id LIMIT 6")
    ids = [row["id"] for row in cur.fetchall()]
    if len(ids) < 5:
        return
    tasks = [
        (ids[0], None, 1, "Courses Monoprix", "Aller au Monoprix chercher une liste de courses legeres. Environ 3-4 sacs.", 48.8570, 2.3530, 8.00),
        (ids[2], None, 2, "Sortir mes poubelles", "Poubelles vertes et jaunes a descendre mardi soir avant 21h.", 48.8540, 2.3505, 3.00),
        (ids[3], None, 7, "Monter une etagere BILLY", "Etagere IKEA BILLY, outils fournis, 2 personnes conseillees.", 48.8590, 2.3610, 12.00),
        (ids[0], None, 3, "Aide demarches CAF", "M'aider a remplir un formulaire CAF en ligne. 1h max.", 48.8558, 2.3510, 10.00),
        (ids[1], None, 5, "Arroser mes plantes", "Absent ce week-end, 10 plantes a arroser une fois. Cle remise.", 48.8610, 2.3475, 4.00),
        (ids[4], None, 6, "Accompagnement pharmacie", "Accompagner jusqu'a la pharmacie rue de la Paix, 10 min a pied.", 48.8545, 2.3440, 6.00),
        (ids[3], None, 4, "Porter cartons au 3e", "3 cartons legers a monter au 3e etage sans ascenseur. 15 min.", 48.8575, 2.3595, 7.00),
        (ids[5], None, 9, "Aide aux devoirs maths", "Lyceen en terminale, exercices de maths a corriger ensemble.", 48.8525, 2.3570, 15.00),
    ]
    for task in tasks:
        cur.execute(
            """INSERT INTO tache
            (demandeur_id,executant_id,categorie_id,titre,description,latitude,longitude,prix)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
            task,
        )
    db.commit()
    print("Taches de demo creees")


def seed_admin(db, cur):
    cur.execute("SELECT COUNT(*) as c FROM utilisateur WHERE email=%s", (ADMIN_EMAIL,))
    if cur.fetchone()["c"] != 0:
        return
    password_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
    cur.execute(
        """INSERT INTO utilisateur
        (nom,prenom,email,mot_de_passe_hash,telephone,latitude,longitude,note_moyenne,nb_avis,est_verifie)
        VALUES('Admin','QuickHelp',%s,%s,'0600000000',48.8566,2.3522,5.0,99,1)""",
        (ADMIN_EMAIL, password_hash),
    )
    db.commit()
    print(f"Compte admin cree - {ADMIN_EMAIL}")
