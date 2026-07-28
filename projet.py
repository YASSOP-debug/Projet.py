#projet_2.py_bot_telegram_avec_gemini

import asyncio
import logging 
import nest_asyncio
from google import genai
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Correctif pour Pydroid 3
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION ---
TOKEN = "8622333887:AAHaQNv4Yw0Iten0SmwNrWm3JWn5oTitrKY"
GEMINI_API_KEY = "AQ.Ab8RN6JsPml9OVXAEhB9368WAl8XwXZBnLABr077UBmnv4z95Q"

# Initialisation avec le SDK officiel
client = genai.Client(api_key=GEMINI_API_KEY)

# --- FONCTION D'APPEL ---
async def demander_gemini(texte_utilisateur):
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash-lite",
            contents=texte_utilisateur
        )
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        
    return "🤖 Oups ! L'API Gemini fait une petite pause. Réessaie dans une minute !"

# --- COMMANDES TELEGRAM ---
async def start(update, context):
    await update.message.reply_text("Salut ! Bot actif et connecté à Gemini !")

async def repondre_message(update, context):
    texte_recu = update.message.text
    message_attente = await update.message.reply_text("🧠 Gemini réfléchit...")
    
    reponse_ai = await demander_gemini(texte_recu)
    
    await message_attente.edit_text(reponse_ai)

# --- LANCEMENT ---
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_message))
    app.run_polling()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
