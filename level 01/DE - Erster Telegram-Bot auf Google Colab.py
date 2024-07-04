# Dieses Skript implementiert einen einfachen Telegram-Bot, der die aktuelle Uhrzeit antwortet, wenn ein Benutzer danach fragt.
# Es verwendet die Bibliothek 'python-telegram-bot', um mit der Telegram-API zu interagieren, und 'nest_asyncio', um die
# Verwendung von asyncio in Umgebungen zu ermöglichen, die dies normalerweise nicht unterstützen, wie z.B. Google Colab.

# Installiere die notwendigen Bibliotheken
!pip install python-telegram-bot nest_asyncio

# Importiere die notwendigen Bibliotheken
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import logging

# Bot-Token, bereitgestellt von BotFather
TOKEN = 'dein-schlüssel'

# Patch anwenden, um die Verwendung von asyncio in Google Colab zu ermöglichen
nest_asyncio.apply()

# Konfiguriere das Logging zur Fehlerbehebung
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Funktion zur Handhabung des /start-Kommandos
# Wenn der Benutzer /start sendet, antwortet der Bot mit einer Willkommensnachricht.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Empfangenes /start-Kommando")
    await update.message.reply_text('Hallo! Sende /time, um die aktuelle Uhrzeit zu erfahren.')

# Funktion zur Handhabung des /time-Kommandos
# Wenn der Benutzer /time sendet, antwortet der Bot mit der aktuellen Uhrzeit.
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Empfangenes /time-Kommando")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await update.message.reply_text(f'Die aktuelle Uhrzeit ist {current_time}')

# Hauptfunktion zum Einrichten und Ausführen des Bots
async def main() -> None:
    logger.info("Initialisierung des Bots")
    app = ApplicationBuilder().token(TOKEN).build()

    # Füge Handler für die Kommandos /start und /time hinzu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time))

    logger.info("Starte Abfrage")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Halte den Bot am Laufen
    logger.info("Bot läuft und wartet auf Kommandos...")
    await asyncio.Future()  # Halte den Bot am Laufen

# Beende alle vorherigen asyncio-Instanzen, um Konflikte zu vermeiden
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

logger.info("Bot wird ausgeführt")
# Führe die Hauptfunktion aus, um den Bot zu starten
asyncio.run(main())
