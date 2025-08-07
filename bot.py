import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive  # Optional for Render

# Load token
load_dotenv()
BOT_TOKEN = os.getenv("8383085554:AAECplHV2Qqj8aGlnjk7Bw3FAAsOrMMvXfg")
DATA_FILE = "data.json"

# Load user data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the NoFap bot!\nUse /master to see your streak.\nUse /streak to check days.\nUse /reset to restart.")

# Reset streak
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    data[user_id] = str(datetime.utcnow())
    save_data(data)
    await update.message.reply_text("🔄 Your streak has been reset!")

# Show streak
async def streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    if user_id not in data:
        await update.message.reply_text("❌ No streak found. Use /reset to start.")
        return
    last_reset = datetime.strptime(data[user_id], "%Y-%m-%d %H:%M:%S.%f")
    days = (datetime.utcnow() - last_reset).days
    await update.message.reply_text(f"🔥 You are {days} days clean!")

# Master command
async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await streak(update, context)

# Bot setup
def main():
    keep_alive()  # optional for uptime
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("streak", streak))
    app.add_handler(CommandHandler("master", master))
    print("🚀 NoFap Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
