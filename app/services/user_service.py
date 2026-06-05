def user_short(user):
    return {
        "id": user["id"],
        "nom": user["nom"],
        "prenom": user["prenom"],
        "email": user["email"],
        "note_moyenne": float(user["note_moyenne"]) if user["note_moyenne"] else 0.0,
        "nb_avis": user["nb_avis"] or 0,
        "est_verifie": bool(user["est_verifie"]),
        "latitude": float(user["latitude"]) if user["latitude"] else 48.8566,
        "longitude": float(user["longitude"]) if user["longitude"] else 2.3522,
    }
