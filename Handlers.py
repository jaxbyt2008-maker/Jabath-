"""
Command and message handlers for the Telegram bot
"""
from telegram import Update
from telegram.ext import ContextTypes
import requests
from datetime import datetime, timedelta
import json

# Weather handler
async def get_weather(city: str) -> str:
    """Get weather information for a city"""
    try:
        # Get coordinates for the city
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geo_response = requests.get(geo_url, params=geo_params, timeout=5)
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return f"❌ City '{city}' not found. Please try another city name."
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        name = location["name"]
        country = location.get("country", "")
        
        # Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_data = weather_response.json()
        
        current = weather_data.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        
        # Weather code interpretation
        weather_code = current.get("weather_code", 0)
        weather_desc = get_weather_description(weather_code)
        
        result = f"""
🌍 **Weather in {name}, {country}**

🌡️ Temperature: {temp}°C
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} km/h
⛅ Condition: {weather_desc}
        """
        return result.strip()
        
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"

def get_weather_description(code: int) -> str:
    """Convert weather code to description"""
    weather_codes = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Foggy rime 🌫️",
        51: "Light drizzle 🌧️",
        53: "Moderate drizzle 🌧️",
        55: "Dense drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain ⛈️",
        71: "Slight snow ❄️",
        73: "Moderate snow ❄️",
        75: "Heavy snow ❄️",
        80: "Slight rain showers 🌧️",
        81: "Moderate rain showers 🌧️",
        82: "Violent rain showers ⛈️",
        85: "Slight snow showers ❄️",
        86: "Heavy snow showers ❄️",
        95: "Thunderstorm ⛈️",
    }
    return weather_codes.get(code, "Unknown")

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_message = f"""
👋 Welcome to jabath_bot, {user.first_name}!

I'm a multi-featured bot that can help you with:
• 🔄 Echo messages
• 🌤️ Check weather in any city
• ⏰ Set reminders
• 🖼️ Process images
• And more!

Use /help to see all available commands.
    """
    await update.message.reply_text(welcome_message.strip())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
📋 **Available Commands:**

/start - Welcome message
/help - Show this help message
/hello - Get a greeting
/weather <city> - Get weather for a city (e.g., /weather London)
/remind <seconds> <message> - Set a reminder (e.g., /remind 60 Drink water)
/echo <text> - Echo back your text
/joke - Get a random joke
/about - About this bot
/contact - Contact information

**Features:**
• 🔄 Echo any message (just send text)
• 🌤️ Real-time weather data
• ⏰ Reminders and scheduling
• 🖼️ Image processing
• 😄 Fun commands

Try any command above!
    """
    await update.message.reply_text(help_message.strip(), parse_mode="Markdown")

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /hello command"""
    user = update.effective_user
    hello_message = f"👋 Hello, {user.first_name}! Nice to meet you! 😊"
    await update.message.reply_text(hello_message)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weather command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /weather <city_name>\nExample: /weather London")
        return
    
    city = " ".join(context.args)
    weather_info = await get_weather(city)
    await update.message.reply_text(weather_info, parse_mode="Markdown")

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /echo command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /echo <text>\nExample: /echo Hello World")
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"🔄 {text}")

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /joke command"""
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        joke_data = response.json()
        joke = f"{joke_data['setup']}\n\n{joke_data['punchline']}"
        await update.message.reply_text(f"😄 {joke}")
    except Exception as e:
        await update.message.reply_text("❌ Could not fetch joke. Try again later!")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_message = """
🤖 **About jabath_bot**

This is a feature-rich Telegram bot built with Python.

**Features:**
✅ Weather information
✅ Echo/message repeating
✅ Reminders and scheduling
✅ Image processing
✅ Fun commands (jokes, etc.)

**Created by:** Jackson John
**Repository:** github.com/jaxbyt/jabath_bot
**Tech:** Python, python-telegram-bot, Open-Meteo API
    """
    await update.message.reply_text(about_message.strip(), parse_mode="Markdown")

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact command"""
    contact_message = """
📧 **Contact Information**

GitHub: @jaxbyt
Email: jaxbyt2008@gmail.com

For bot issues or suggestions, please visit:
github.com/jaxbyt/jabath_bot

Happy to help! 😊
    """
    await update.message.reply_text(contact_message.strip(), parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages (echo feature)"""
    message_text = update.message.text
    user = update.effective_user
    
    # Echo the message
    echo_message = f"🔄 {user.first_name}, you said: \"{message_text}\""
    await update.message.reply_text(echo_message)

async def handle_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Handle reminder notifications"""
    job = context.job
    chat_id = job.chat_id
    message = job.data
    
    reminder_text = f"⏰ **Reminder:** {message}"
    await context.bot.send_message(chat_id=chat_id, text=reminder_text, parse_mode="Markdown")

async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /remind command"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /remind <seconds> <message>\n"
            "Example: /remind 60 Drink water"
        )
        return
    
    try:
        seconds = int(context.args[0])
        message = " ".join(context.args[1:])
        
        # Schedule the reminder
        context.job_queue.run_once(
            handle_reminder,
            when=timedelta(seconds=seconds),
            chat_id=update.effective_chat.id,
            data=message,
            name=f"reminder_{update.effective_chat.id}_{datetime.now().timestamp()}"
        )
        
        await update.message.reply_text(
            f"⏰ Reminder set for {seconds} seconds from now!\n"
            f"📝 Message: {message}"
        )
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number of seconds!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error setting reminder: {str(e)}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    user = update.effective_user
    await update.message.reply_text(
        f"📸 Thanks for the photo, {user.first_name}!\n"
        f"Photo ID: {update.message.photo[-1].file_id}"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again later."
      )
