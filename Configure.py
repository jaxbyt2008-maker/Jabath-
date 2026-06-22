# Telegram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Bot token from @BotFather
BOT_TOKEN = "8358621792:AAEIRQ9yx9rCHMpXeJA3dIiaZHy233ecAAA"

# Weather API (using Open-Meteo - free, no key needed)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Bot settings
BOT_NAME = "jabath_bot"
ADMIN_ID = None  # Set your Telegram user ID here if needed

# Features toggle
FEATURES = {
    "echo": True,
    "commands": True,
    "weather": True,
    "reminders": True,
    "image_processing": True,
}
