from config import API_TOKEN
import telebot 
bot = telebot.TeleBot(token=API_TOKEN)

help_message  = (
    "/start - Start the bot\n"
    "/help  - Show this help message\n"
    "\nYou can also type your city and country code to get weather info.\n"
    "Example: Dhaka,BD"
)

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = f'Welcome {message.from_user.first_name}  ! Type your city and Country code to get weather info(example:Dhaka,BD)'
    bot.send_message(message.chat.id,welcome_text)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id , help_message);

@bot.message_handler(func=lambda message:True)
def reply_func(message):
    bot.reply_to(message, text= help_message)




bot.polling()
