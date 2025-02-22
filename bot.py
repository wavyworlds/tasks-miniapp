
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your bot token
BOT_TOKEN = "7532214010:AAGuuMOa2G708Ah4O3uhkgS0KaTwgR5TaEs"
bot = telebot.TeleBot(BOT_TOKEN)

# Main menu keyboard
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("💰 Balance"), KeyboardButton("🔗 Refer"))
    markup.add(KeyboardButton("💵 Withdraw"), KeyboardButton("🎥 Tasks"))
    markup.add(KeyboardButton("📞 Contact Admin"))
    return markup

# Inline keyboard for Contact Admin
def contact_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("WhatsApp", url="https://wa.me/+233549699649"))
    markup.add(InlineKeyboardButton("Telegram", url="https://t.me/wavyads"))
    markup.add(InlineKeyboardButton("YouTube", url="https://youtube.com/@clangzero?si=fsGZtYJvq9HeGAVD"))
    markup.add(InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@wizzay1"))
    return markup

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Tube Earning Bot! 🎉", reply_markup=main_menu())

# Handle main menu buttons
@bot.message_handler(func=lambda message: message.text in ["💰 Balance", "🔗 Refer", "💵 Withdraw", "🎥 Tasks", "📞 Contact Admin"])
def handle_buttons(message):
    if message.text == "📞 Contact Admin":
        bot.send_message(message.chat.id, "📞 *Choose Medium*", parse_mode="Markdown", reply_markup=contact_admin())
    elif message.text == "💰 Balance":
        bot.send_message(message.chat.id, "💰 Your balance:\n- Referrals: 0 GHS\n- Tasks: 0 GHS\n- Total: 0 GHS")
    elif message.text == "🔗 Refer":
        bot.send_message(message.chat.id, "🔗 Your referral link: [generated_link_here]")
    elif message.text == "💵 Withdraw":
        bot.send_message(message.chat.id, "💵 Choose withdrawal method:\n1️⃣ Mobile Money (MoMo)\n2️⃣ USDT (BEP20)")
    elif message.text == "🎥 Tasks":
        bot.send_message(message.chat.id, "🎥 Click the button below to complete tasks:", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Go to Tasks", url="https://tubeearningtasks.netlify.app")))

# Run the bot
bot.polling()
