import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive

DATA_FILE = "data.json"
BOT_TOKEN = "8383085554:AAECplHV2Qqj8aGlnjk7Bw3FAAsOrMMvXfg"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to NoFap Tracker!\nUse /streak to check your progress.")

async def streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    today = get_today()

    if user_id not in data:
        data[user_id] = {"last_reset": today, "streak": 0}
    else:
        last = datetime.strptime(data[user_id]["last_reset"], "%Y-%m-%d")
        days = (datetime.now() - last).days
        data[user_id]["streak"] = days

    save_data(data)
    await update.message.reply_text(f"🔥 Your current streak is: {data[user_id]['streak']} days")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    today = get_today()

    data[user_id] = {"last_reset": today, "streak": 0}
    save_data(data)
    await update.message.reply_text("💀 Streak reset. Start fresh from today!")

async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    leaderboard = sorted(data.items(), key=lambda x: x[1].get("streak", 0), reverse=True)
    top10 = leaderboard[:10]

    msg = "🏆 Top Streaks:\n"
    for i, (uid, info) in enumerate(top10, 1):
        msg += f"{i}. {uid}: {info['streak']} days\n"

    await update.message.reply_text(msg)

# Keep alive and run bot
keep_alive()

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("streak", streak))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("master", master))

app.run_polling()
