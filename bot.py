# bot.py
import logging
import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configure logging for debugging purposes
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(_name_)

# Use environment variables or replace with your actual tokens/URLs directly
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
# Replace with your actual server URL where webhook.py is hosted
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-heroku-app.herokuapp.com/webhook")

def start(update, context):
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text(
        "Hi! Send me a query like 'Find details of Sundar Pichai' or 'Email of Sam Altman'."
    )

def handle_message(update, context):
    """
    Forwards the user's text message to the webhook for processing.
    """
    user_input = update.message.text
    chat_id = update.message.chat_id

    # Prepare payload to send to webhook
    payload = {
        "text": user_input,
        "chat_id": chat_id
    }

    try:
        # Send the payload to the webhook endpoint
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            update.message.reply_text("Processing your request...")
        else:
            update.message.reply_text("There was an error processing your request.")
    except Exception as e:
        logger.error("Error connecting to webhook: %s", e)
        update.message.reply_text("Error connecting to processing server.")

def handle_voice(update, context):
    """
    Downloads voice messages, converts them to text, and sends the text for processing.
    """
    voice = update.message.voice
    file = context.bot.getFile(voice.file_id)
    file_path = "voice_message.ogg"
    file.download(file_path)

    # Placeholder function for voice-to-text conversion; implement your own API call here
    transcribed_text = convert_voice_to_text(file_path)

    payload = {"text": transcribed_text, "chat_id": update.message.chat_id}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            update.message.reply_text("Processing your voice request...")
        else:
            update.message.reply_text("There was an error processing your voice request.")
    except Exception as e:
        logger.error("Error connecting to webhook: %s", e)
        update.message.reply_text("Error connecting to processing server.")

def convert_voice_to_text(file_path):
    """
    Dummy voice-to-text conversion.
    Replace this with an actual integration to a Speech-to-Text API (e.g., Google Cloud Speech-to-Text).
    """
    # For now, simply return a placeholder text.
    return "Transcribed text from voice message."

def main():
    # Initialize the Telegram bot
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    # Start polling for messages
    updater.start_polling()
    updater.idle()

if _name_ == '_main_':
    main()