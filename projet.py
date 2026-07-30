#projet_2.py_bot_telegram_avec_gemini

import asyncio
import logging 
import nest_asyncio
import json
import os
import time
from google import genai
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Correctif pour Pydroid 3
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION ---
TOKEN = "8622333887:AAHaQNv4Yw0Iten0SmwNrWm3JWn5oTitrKYAQ.Ab8RN6JsPml9OVXAEhB9368WAl8XwXZBnLABr077UBmnv4z95Q"
GEMINI_API_KEY = "AQ.Ab8RN6JsPml9OVXAEhB9368WAl8XwXZBnLABr077UBmnv4z95Q"

# Initialisation avec le SDK officiel
client = genai.Client(api_key=GEMINI_API_KEY)

# Liste des modèles à utiliser pour la bascule
LISTE_MODELES = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

# Dossier de stockage des mémoires
CHEMIN_MEMOIRE = "memoires/memoires_ia"
os.makedirs(CHEMIN_MEMOIRE, exist_ok=True)
DELAI_PURGE_HISTORIQUE = 3 * 24 * 60 * 60  # 3 jours en secondes

# --- FONCTIONS DE GESTION D'HISTORIQUE ---
def obtenir_chemin_historique(id_chat):
    return os.path.join(CHEMIN_MEMOIRE, f"{id_chat}.json")

def lire_historique(id_chat):
    chemin = obtenir_chemin_historique(id_chat)
    if not os.path.exists(chemin):
        return []
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            historique = json.load(f)
        maintenant = time.time()
        # Purge des vieux messages
        return [msg for msg in historique if (maintenant - msg.get("horodatage", 0)) < DELAI_PURGE_HISTORIQUE]
    except Exception:
        return []

def sauvegarder_historique(id_chat, historique):
    chemin = obtenir_chemin_historique(id_chat)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=2, ensure_ascii=False)

# --- FONCTION D'APPEL ---
async def demander_gemini(id_chat, texte_utilisateur):
    historique = lire_historique(id_chat)

    # Préparation de l'historique pour l'API Gemini
    contenu_historique = []
    for msg in historique:
        contenu_historique.append({
            "role": msg["role"],
            "parts": [{"text": msg["texte"]}]
        })

    # On itère sur chaque modèle disponible
    for nom_modele in LISTE_MODELES:
        try:
            # Création du chat avec l'historique
            chat = client.chats.create(model=nom_modele, history=contenu_historique)
            response = await asyncio.to_thread(chat.send_message, texte_utilisateur)

            if response and response.text:
                # Mise à jour de l'historique
                historique.append({"role": "user", "texte": texte_utilisateur, "horodatage": time.time()})
                historique.append({"role": "model", "texte": response.text, "horodatage": time.time()})
                sauvegarder_historique(id_chat, historique)
                return response.text
        except Exception as e:
            print(f"⚠️ AVERTISSEMENT : Erreur avec {nom_modele} : {e}")
            continue

    return "🤖 Oups ! Tous les modèles Gemini font une pause. Réessaie dans une minute !"

# --- FONCTION DE DECOUPAGE ---
def decouper_message(texte, limite=4000):
    """Découpe un texte en plusieurs messages pour respecter la limite de Telegram."""
    if len(texte) <= limite:
        return [texte]

    fragments = []
    while len(texte) > limite:
        # Chercher le dernier saut de ligne dans la limite pour éviter de couper un mot
        index_coupe = texte.rfind('\n', 0, limite)
        if index_coupe == -1:
            index_coupe = limite

        fragments.append(texte[:index_coupe].strip())
        texte = texte[index_coupe:].strip()

    fragments.append(texte)
    return fragments

# --- COMMANDES TELEGRAM ---
async def start(update, context):
    await update.message.reply_text("Salut ! Bot actif et connecté à Gemini !")

async def repondre_message(update, context):
    id_chat = str(update.message.chat_id)
    texte_recu = update.message.text
    message_attente = await update.message.reply_text("🧠 Gemini réfléchit...")

    reponse_ai = await demander_gemini(id_chat, texte_recu)

    # Découper la réponse si nécessaire
    fragments = decouper_message(reponse_ai)

    # Envoyer le premier fragment en modifiant le message d'attente
    await message_attente.edit_text(fragments[0])

    # Envoyer les fragments suivants s'il y en a
    for fragment in fragments[1:]:
        await update.message.reply_text(fragment)

# --- LANCEMENT ---
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_message))
    app.run_polling()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
