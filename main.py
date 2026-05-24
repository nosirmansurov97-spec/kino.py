import telebot
import json
import os
from datetime import datetime

TOKEN = os.environ["TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

bot = telebot.TeleBot(TOKEN)

MOVIES_FILE = "movies.json"
USERS_FILE = "users.json"

if not os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_movies():
    with open(MOVIES_FILE, "r") as f:
        return json.load(f)

def save_movies(data):
    with open(MOVIES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user):
    users = load_users()
    uid = str(user.id)
    users[uid] = {
        "name": user.first_name,
        "date": str(datetime.now().date())
    }
    save_users(users)

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)
    users = load_users()
    total_users = len(users)
    bot.send_message(
        message.chat.id,
        f"""
🎬 Xush kelibsiz!

📥 Kino kodini yuboring.

👥 Foydalanuvchilar: {total_users}
        """
    )

@bot.message_handler(content_types=['video'])
def save_movie(message):
    if message.from_user.id != ADMIN_ID:
        return
    movies = load_movies()
    code = str(len(movies) + 100)
    movies[code] = message.video.file_id
    save_movies(movies)
    bot.reply_to(
        message,
        f"""
✅ Kino saqlandi!

🎬 Kino kodi: {code}
        """
    )

@bot.message_handler(func=lambda m: True)
def send_movie(message):
    code = message.text.strip()
    movies = load_movies()
    if code in movies:
        bot.send_video(
            message.chat.id,
            movies[code],
            caption=f"🎬 Kino kodi: {code}"
        )
    else:
        bot.reply_to(
            message,
            "❌ Bunday kino topilmadi."
        )

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    users = load_users()
    total = len(users)
    today = str(datetime.now().date())
    today_users = sum(1 for u in users.values() if u["date"] == today)
    bot.send_message(
        message.chat.id,
        f"""
📊 BOT STATISTIKASI

👥 Jami foydalanuvchilar: {total}

📅 Bugungi foydalanuvchilar: {today_users}
        """
    )

print("🎬 Kino bot ishga tushdi...")
bot.infinity_polling()
