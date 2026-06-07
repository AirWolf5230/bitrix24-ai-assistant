from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.bot.handlers import start, handle_message
from app.config import TELEGRAM_BOT_TOKEN


def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    print("Бот запущен")

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    app.run_polling(drop_pending_updates=True)