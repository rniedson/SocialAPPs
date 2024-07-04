# यह स्क्रिप्ट एक सरल टेलीग्राम बॉट को लागू करती है जो उपयोगकर्ता द्वारा अनुरोध करने पर वर्तमान समय का उत्तर देती है।
# यह 'python-telegram-bot' लाइब्रेरी का उपयोग टेलीग्राम API के साथ बातचीत करने के लिए करता है और 'nest_asyncio' का उपयोग करता है
# उन परिवेशों में asyncio उपयोग को सक्षम करने के लिए जो आम तौर पर इसका समर्थन नहीं करते, जैसे कि Google Colab।

# आवश्यक लाइब्रेरी स्थापित करें
!pip install python-telegram-bot nest_asyncio

# आवश्यक लाइब्रेरी आयात करें
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import logging

# BotFather द्वारा प्रदत्त बॉट टोकन
TOKEN = 'आपकी-चाबी'

# Google Colab में asyncio उपयोग की अनुमति देने के लिए पैच लागू करें
nest_asyncio.apply()

# डिबगिंग के लिए लॉगिंग कॉन्फ़िगर करें
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start कमांड को हैंडल करने के लिए फ़ंक्शन
# जब उपयोगकर्ता /start भेजता है, तो बॉट एक स्वागत संदेश के साथ उत्तर देता है।
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("प्राप्त /start कमांड")
    await update.message.reply_text('नमस्ते! वर्तमान समय जानने के लिए /time भेजें।')

# /time कमांड को हैंडल करने के लिए फ़ंक्शन
# जब उपयोगकर्ता /time भेजता है, तो बॉट वर्तमान समय के साथ उत्तर देता है।
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("प्राप्त /time कमांड")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await update.message.reply_text(f'वर्तमान समय {current_time} है')

# बॉट को सेटअप और चलाने के लिए मुख्य फ़ंक्शन
async def main() -> None:
    logger.info("बॉट को प्रारंभ करना")
    app = ApplicationBuilder().token(TOKEN).build()

    # /start और /time कमांड के लिए हैंडलर जोड़ें
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time))

    logger.info("पोलिंग शुरू करना")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # बॉट को चालू रखें
    logger.info("बॉट चल रहा है, कमांड की प्रतीक्षा कर रहा है...")
    await asyncio.Future()  # बॉट को चालू रखें

# टकराव से बचने के लिए किसी भी पिछले asyncio इंस्टेंस को समाप्त करें
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

logger.info("बॉट चल रहा है")
# बॉट को शुरू करने के लिए मुख्य फ़ंक्शन को निष्पादित करें
asyncio.run(main())
