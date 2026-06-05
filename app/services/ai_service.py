import json
import random
import urllib.request


def suggest_text(req):
    if req.api_key and len(req.api_key) > 10:
        try:
            prompt = (
                f"Genere une description courte (max 80 mots) pour une micro-tache : {req.context}. Francais, direct, rassurant."
                if req.type == "mission"
                else f"Genere un avis ({req.note}/5 etoiles) pour cette mission : {req.context}. Max 50 mots, naturel, francais."
            )
            body = json.dumps(
                {
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 200,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ).encode()
            request = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=body,
                headers={
                    "x-api-key": req.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read())
                return {"success": True, "text": data["content"][0]["text"], "source": "claude"}
        except Exception:
            pass

    context = req.context or "cette tache"
    if req.type == "mission":
        text = random.choice(
            [
                f"Besoin d'aide pour {context}. Tache simple, aucune competence particuliere requise. Intervention rapide, bien remuneree.",
                f"Je recherche quelqu'un de disponible pour {context}. Mission courte et accessible a tous.",
                f"Aide ponctuelle souhaitee : {context}. Disponible rapidement. Paiement via QuickHelp.",
            ]
        )
    else:
        note = max(1, min(5, req.note or 5))
        text = random.choice(
            {
                5: [
                    "Parfait ! Personne ponctuelle, efficace et tres agreable. Je recommande vivement !",
                    "Excellente prestation, mission accomplie rapidement et avec soin. Tres satisfait(e) !",
                ],
                4: [
                    "Bonne prestation, mission bien realisee. Legerement en retard mais rien de grave.",
                    "Tres bien, je suis satisfait(e). Communication claire et travail soigne.",
                ],
                3: [
                    "Service correct, la mission a ete realisee. Quelques ajustements auraient ete apprecies.",
                    "Prestation honnete. Le travail a ete fait, sans plus.",
                ],
                2: ["Mission realisee mais communication difficile. Resultat en deca des attentes."],
                1: ["Experience decevante. La tache n'a pas ete realisee comme prevu."],
            }[note]
        )
    return {"success": True, "text": text, "source": "template"}
