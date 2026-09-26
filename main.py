import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! البوت راه يمشي ✅")

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 الدورات:\n1. تجويد\n2. البقرة\n3. ال عمران\n4. النساء\n5. المائدة\n6. الكهف\n7. التفسير\n8. تصحيح")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", courses))

print("Bot is running...")
app.run_polling()
