import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# التوكن من Render
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("السلام عليكم! بوت مقرأة نور يرحب بكم 🌙")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب /start للبداية")

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN غير موجود!")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    print("البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
