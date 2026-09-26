import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7697171173
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "admins": [7697171173],
    "courses": ["تجويد", "البقرة", "آل عمران", "النساء", "المائدة", "الكهف", "التفسير", "تصحيح و تدقيق"],
    "tag_message": "📢 يا أهل القرآن تعالو! عندنا حصة جديدة في مقرأة النور 🌸",
    "remind_time": "20:00",
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=2)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        s = json.load(f)
        if "admins" not in s: s["admins"] = [OWNER_ID]
        return s

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(s, f, ensure_ascii=False, indent=2)

# /start
async def start(update, context):
    text = "🌸 أهلا بك في مقرأة النور!\n\n📚 /courses - الدورات\n👥 /tagall - منشن البنات\n🎧 /playquran - تشغيل قرآن\n⚙️ /settings - لوحة التحكم (للإدارة)"
    await update.message.reply_text(text)

# /courses
async def courses_cmd(update, context):
    s = load_settings()
    keyboard = [[InlineKeyboardButton(f"📚 {c}", callback_data=f"course_{c}")] for c in s["courses"]]
    await update.message.reply_text("📚 قائمة الدورات:", reply_markup=InlineKeyboardMarkup(keyboard))

# /tagall
async def tagall_cmd(update, context):
    s = load_settings()
    if update.effective_user.id not in s["admins"]:
        await update.message.reply_text("⛔ للإدارة فقط!"); return
    await update.message.reply_text(s["tag_message"])

# /playquran
async def playquran_cmd(update, context):
    surah = " ".join(context.args) if context.args else "البقرة"
    keyboard = [[InlineKeyboardButton(f"▶️ تشغيل سورة {surah}", url=f"https://www.youtube.com/results?search_query=سورة+{surah}+المنشاوي")]]
    await update.message.reply_text(f"🎧 سورة {surah} - جاهزة للبث:", reply_markup=InlineKeyboardMarkup(keyboard))

# /settings
async def settings_cmd(update, context):
    s = load_settings()
    if update.effective_user.id not in s["admins"]:
        await update.message.reply_text("⛔ هادي للإدارة فقط يا آمال!"); return
    admins_list = "\n".join([f"• {a}" for a in s["admins"]])
    keyboard = [
        [InlineKeyboardButton("➕ إضافة مشرفة", callback_data="add_admin")],
        [InlineKeyboardButton("➖ حذف مشرفة", callback_data="remove_admin")],
        [InlineKeyboardButton("📋 قائمة المشرفات", callback_data="list_admins")],
        [InlineKeyboardButton("👥 تعديل رسالة الطاڨ", callback_data="edit_tag")],
        [InlineKeyboardButton("⏰ تعديل وقت التذكير", callback_data="edit_time")],
    ]
    await update.message.reply_text(f"⚙️ لوحة تحكم مقرأة النور\n\n👤 المشرفات:\n{admins_list}", reply_markup=InlineKeyboardMarkup(keyboard))

# الأزرار
async def buttons(update, context):
    q = update.callback_query; await q.answer()
    s = load_settings()
    if q.data == "add_admin":
        context.user_data["waiting_for"] = "add_admin"
        await q.message.reply_text("📩 ابعثيلي آيدي المشرفة الجديدة:\n(جيبيه من @userinfobot)\nمثال: 123456789")
    elif q.data == "remove_admin":
        context.user_data["waiting_for"] = "remove_admin"
        await q.message.reply_text("ابعثيلي آيدي المشرفة اللي تحبي تحذفيها:")
    elif q.data == "list_admins":
        admins_list = "\n".join([f"👤 {a}" for a in s["admins"]])
        await q.message.reply_text(f"📋 قائمة المشرفات:\n{admins_list}")
    elif q.data == "edit_tag":
        context.user_data["waiting_for"] = "tag"
        await q.message.reply_text("ابعثيلي رسالة الطاڨ الجديدة:")
    elif q.data == "edit_time":
        context.user_data["waiting_for"] = "time"
        await q.message.reply_text("ابعثيلي الوقت الجديد مثلا 21:00:")
    elif q.data.startswith("course_"):
        await q.message.reply_text(f"🌸 دخلتي لدورة {q.data.replace('course_','')}")

# حفظ التعديلات
async def save_edit(update, context):
    if "waiting_for" not in context.user_data: return
    s = load_settings()
    text = update.message.text.strip()
    waiting = context.user_data["waiting_for"]

    if waiting == "add_admin":
