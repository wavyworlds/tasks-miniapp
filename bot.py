import os
import telebot

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Tube Earning Bot! Watch videos, complete tasks, and earn rewards.")

@bot.message_handler(commands=["task"])
def send_task(message):
    video_links = [
        "https://youtube.com/shorts/v0vNYgGxg0w?feature=share",
        "https://youtube.com/shorts/ew6Zxy1Amsw?feature=share",
        "https://youtube.com/shorts/d6Cut_VS5wc?feature=share",
        "https://youtu.be/QHUqTNNDduI",
        "https://youtu.be/ocoAJvXIfe8"
    ]
    
    task_message = "Complete the following video tasks:\n\n"
    for idx, link in enumerate(video_links, start=1):
        task_message += f"{idx}. [Watch Video]({link})\n"
    
    bot.send_message(message.chat.id, task_message, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Use /task to get video tasks.")

bot.polling()
