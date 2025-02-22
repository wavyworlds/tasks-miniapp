from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, ConversationHandler
import re

TOKEN = "7532214010:AAGuuMOa2G708Ah4O3uhkgS0KaTwgR5TaEs"
BOT_USERNAME = "tubeearningbot"
ADMIN_CHAT_ID = -1002450573840  # Replace with your admin group/channel ID

# User data storage
user_data = {}

# Wallet states
(WALLET_MENU, MOMO_NAME, MOMO_NETWORK, MOMO_NUMBER, USDT_ADDRESS, WITHDRAW_AMOUNT) = range(6)

# Referral system
def start(update, context):
    user = update.message.from_user
    referrer_id = update.message.text.split()[-1] if len(update.message.text.split()) > 1 else None
    
    if referrer_id and referrer_id.isdigit() and int(referrer_id) != user.id:
        referrer_id = int(referrer_id)
        user_data.setdefault(referrer_id, {"referrals": 0, "referral_earnings": 0})
        user_data[referrer_id]["referrals"] += 1
        user_data[referrer_id]["referral_earnings"] += 1
        context.bot.send_message(referrer_id, f"🎉 Someone just joined using your referral link! You earned **1 GHS**.")
        context.bot.send_message(ADMIN_CHAT_ID, f"🚀 New user joined: @{user.username} via referral.")

    main_menu(update, context)

def main_menu(update, context):
    keyboard = [
        [KeyboardButton("💰 Balance"), KeyboardButton("👥 Refer")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🎯 Tasks")],
        [KeyboardButton("🔑 Wallet"), KeyboardButton("📞 Contact Admin")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("🏠 *Main Menu*", reply_markup=reply_markup, parse_mode="Markdown")

def balance(update, context):
    user = update.message.from_user
    balance = user_data.get(user.id, {}).get("balance", 0)
    referral_earnings = user_data.get(user.id, {}).get("referral_earnings", 0)
    task_earnings = balance - referral_earnings

    update.message.reply_text(
        f"💰 *Your Balance:*\n\n"
        f"👥 Referral Earnings: *{referral_earnings} GHS*\n"
        f"🎯 Task Earnings: *{task_earnings} GHS*\n"
        f"📊 Total Balance: *{balance} GHS*",
        parse_mode="Markdown"
    )

def refer(update, context):
    user = update.message.from_user
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user.id}"
    referrals = user_data.get(user.id, {}).get("referrals", 0)
    earnings = user_data.get(user.id, {}).get("referral_earnings", 0)

    update.message.reply_text(
        f"👥 *Your Referral Link:*\n{referral_link}\n\n"
        f"✅ *Total Invites:* {referrals}\n"
        f"💸 *Earnings from Referrals:* {earnings} GHS",
        parse_mode="Markdown"
    )

def wallet(update, context):
    keyboard = [
        [KeyboardButton("📱 MoMo"), KeyboardButton("💰 USDT (BEP20)")],
        [KeyboardButton("⬅️ Back to Menu")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("💳 *Set up your wallet:*", reply_markup=reply_markup, parse_mode="Markdown")

def set_momo(update, context):
    update.message.reply_text("🔤 *Enter your MoMo name:*", parse_mode="Markdown")
    return MOMO_NAME

def momo_name(update, context):
    user_data[update.message.from_user.id] = {"momo_name": update.message.text}
    update.message.reply_text("📡 *Choose your network:* (MTN, Telecel, Tigo)")
    return MOMO_NETWORK

def momo_network(update, context):
    network = update.message.text.upper()
    if network not in ["MTN", "TELECEL", "TIGO"]:
        update.message.reply_text("❌ *Invalid network! Choose MTN, Telecel, or Tigo.*")
        return MOMO_NETWORK

    user_data[update.message.from_user.id]["momo_network"] = network
    update.message.reply_text("📞 *Enter your MoMo number:*")
    return MOMO_NUMBER

def momo_number(update, context):
    user_data[update.message.from_user.id]["momo_number"] = update.message.text
    update.message.reply_text("✅ *MoMo details saved!*")
    return ConversationHandler.END

def set_usdt(update, context):
    update.message.reply_text("💰 *Enter your USDT (BEP20) address:*")
    return USDT_ADDRESS

def usdt_address(update, context):
    address = update.message.text
    if not re.match(r"^0x[a-fA-F0-9]{40}$", address):
        update.message.reply_text("❌ *Invalid BEP20 address! Try again.*")
        return USDT_ADDRESS

    user_data[update.message.from_user.id] = {"usdt_address": address}
    update.message.reply_text("✅ *USDT Address saved!*")
    return ConversationHandler.END

def withdraw(update, context):
    update.message.reply_text("💰 *Enter amount to withdraw (Minimum: 10 GHS):*")
    return WITHDRAW_AMOUNT

def withdraw_amount(update, context):
    user = update.message.from_user
    amount = int(update.message.text)
    balance = user_data.get(user.id, {}).get("balance", 0)

    if amount < 10:
        context.bot.send_message("@craybadreqs", f"❌ Withdrawal failed for @{user.username}: Amount too low.")
        update.message.reply_text("❌ Minimum withdrawal is 10 GHS.")
        return ConversationHandler.END

    if amount > balance:
        update.message.reply_text("❌ Insufficient balance.")
        return ConversationHandler.END

    user_data[user.id]["balance"] -= amount
    context.bot.send_message("@zayandsalaama", f"🔔 Withdrawal request: {amount} GHS from @{user.username}.")
    update.message.reply_text("✅ Withdrawal request submitted.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", main_menu))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("refer", refer))
    dp.add_handler(CommandHandler("wallet", wallet))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
