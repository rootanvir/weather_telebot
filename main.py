from config import API_TOKEN, WEATHER_API_KEY
import telebot
import requests
from datetime import timezone 
from datetime import datetime
bot = telebot.TeleBot(API_TOKEN)

HELP_MESSAGE = (
    "/start   - Start the bot\n"
    "/help    - Show this help message\n"
    "/weather <city>,<country code (optional)> - Get current weather\n"
    "We don't ask location access ! \n\n"
    "Example: /weather Dhaka,BD"
)

@bot.message_handler(commands=['start'])
def welcome(message):
    text = f'Welcome {message.from_user.first_name}! 👋\n\n' \
           'Type your city and country code to get weather info.\n' \
           'Example: Dhaka,BD'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['weather'])
def weather_command(message):
    try:
        cmd = message.text.strip()
        if len(cmd.split()) < 2:
            bot.reply_to(message, "❌ Please provide a city.\nExample: /weather Dhaka,BD")
            return

        city = cmd.split(maxsplit=1)[1].strip()

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "en"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 404:
            bot.reply_to(message, f"❌ City '{city}' not found.")
            return
        elif response.status_code == 401:
            bot.reply_to(message, "❌ Invalid WEATHER_API_KEY. Check your config.py")
            return
        elif response.status_code != 200:
            error_msg = data.get("message", "Unknown error")
            bot.reply_to(message, f"❌ API Error: {error_msg}")
            return

        # Extract data
        city_name = data["name"]
        country = data["sys"]["country"]
        temp = round(data["main"]["temp"], 1)
        feels_like = round(data["main"]["feels_like"], 1)
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()
        wind_speed = data["wind"]["speed"]

       

        timezone_offset = data.get("timezone", 0)
        sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"] + timezone_offset, tz=timezone.utc).strftime('%I:%M %p')
        sunset_time = datetime.fromtimestamp(data["sys"]["sunset"] + timezone_offset, tz=timezone.utc).strftime('%I:%M %p')
        
        weather_text = f"🌤️ **Weather in {city_name}, {country}**\n\n" \
                       f"🌡️**Temperature:** {temp}°C\n" \
                       f"♨️**Feels like:** {feels_like}°C\n" \
                       f"🌤️**Condition:** {description}\n" \
                       f"🌡**Pressure:** {pressure} hPa\n" \
                       f"💧**Humidity:** {humidity}%\n" \
                       f"💨**Wind:** {wind_speed} m/s\n\n" \
                       f"🌅 **Sunrise:** {sunrise_time}\n" \
                       f"🌇 **Sunset:** {sunset_time}"

        bot.reply_to(message, weather_text, parse_mode="Markdown")

    except requests.exceptions.Timeout:
        bot.reply_to(message, "⏳ Request timed out. Please try again.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Something went wrong: {str(e)}")

@bot.message_handler(func=lambda message: True)
def reply_func(message):
    if not message.text.startswith('/'):
        bot.reply_to(message, "I only understand these commands:\n\n" + HELP_MESSAGE)

bot.polling(non_stop=True)