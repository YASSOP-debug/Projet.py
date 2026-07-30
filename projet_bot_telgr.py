#projet_2.py_bot_telegram_avec_gemini

import asyncio
import logging 
import nest_asyncio
import aiohttp
import json
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Correctif pour Pydroid 3 (Android)
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION DES CLÉS ---
TOKEN = "8622333887:AAHaQNv4Yw0Iten0SmwNrWm3JWn5oTitrKY"
GEMINI_API_KEY = "AQ.Ab8RN6JhvYTw2zRVF-DeE02pI88dM5olL6RG0NoM9XevOax3Hg"


# --- FONCTION D'APPEL À GEMINI VIA AIOHTTP ---
async def demander_gemini(texte_utilisateur):
    # Nom exact du modèle reconnu par l'API v1beta
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": texte_utilisateur}
                ]
            }
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=15) as response:
                if response.status == 200:
                    resultat = await response.json()
                    return resultat['candidates'][0]['content']['parts'][0]['text']
                else:
                    erreur_detailee = await response.text()
                    print(f"Erreur API ({response.status}): {erreur_detailee}")
                    return f"Erreur Gemini ({response.status}). Vérifie la clé ou la connexion."
    except Exception as e:
        print(f"Erreur Exception: {e}")
        return "Problème de délai de connexion (Timeout)."

# --- GESTION DES MESSAGES TELEGRAM ---
async def start(update, context):
    await update.message.reply_text("Salut ! Je suis ton bot relié à Gemini. Pose-moi n'importe quelle question !")

async def repondre_message(update, context):
    texte_recu = update.message.text
    
    # Message temporaire pour faire patienter l'utilisateur
    message_attente = await update.message.reply_text("🧠 Gemini réfléchit...")
    
    # Récupération de la réponse de l'IA
    reponse_ai = await demander_gemini(texte_recu)
    
    # Remplacement du message d'attente par la réponse finale
    await message_attente.edit_text(reponse_ai)


# --- DÉMARRAGE DU BOT ---
async def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_message))
    
    await app.run_polling()


# Lancement adapté à l'environnement Pydroid 3
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
