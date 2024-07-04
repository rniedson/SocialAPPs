# このスクリプトは、ユーザーからのプロンプトに応じて現在の時刻を返すシンプルなTelegramボットを実装します。
# 'python-telegram-bot'ライブラリを使用してTelegram APIと対話し、Google Colabなどの通常はサポートされていない環境で
# asyncioの使用を可能にするために'nest_asyncio'を使用します。

# 必要なライブラリをインストール
!pip install python-telegram-bot nest_asyncio

# 必要なライブラリをインポート
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import logging

# BotFatherから提供されたボットトークン
TOKEN = 'あなたのキー'

# Google Colabでasyncioの使用を許可するためにパッチを適用
nest_asyncio.apply()

# デバッグのためにログを設定
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /startコマンドを処理する関数
# ユーザーが/startを送信すると、ボットがウェルカムメッセージで応答します。
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("受信した/startコマンド")
    await update.message.reply_text('こんにちは！現在の時刻を知るには/timeを送信してください。')

# /timeコマンドを処理する関数
# ユーザーが/timeを送信すると、ボットが現在の時刻で応答します。
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("受信した/timeコマンド")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await update.message.reply_text(f'現在の時刻は {current_time} です')

# ボットを設定して実行するためのメイン関数
async def main() -> None:
    logger.info("ボットの初期化")
    app = ApplicationBuilder().token(TOKEN).build()

    # /startと/timeコマンドのハンドラを追加
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time))

    logger.info("ポーリングの開始")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # ボットを実行し続ける
    logger.info("ボットが実行中です。コマンドを待っています...")
    await asyncio.Future()  # ボットを実行し続ける

# 競合を避けるために以前のasyncioインスタンスを終了
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

logger.info("ボットの実行")
# ボットを開始するためにメイン関数を実行
asyncio.run(main())
