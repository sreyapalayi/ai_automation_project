# bot.py
import logging
import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configure logging to help with debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(_name_)

# Environment variables for sensitive info (or replace directly with strings)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://<your-server-address>:5000/webhook")

def start(update, context):
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text(
        "Hi! Send me a query like 'Find details of Sundar Pichai' or 'Email of Sam Altman'."
    )

def handle_message(update, context):
    """
    Forward the user's message to the webhook for processing.
    The webhook will perform the Apollo lookup and logging.
    """
    user_input = update.message.text
    chat_id = update.message.chat_id

    # Prepare payload to send to the webhook
    payload = {
        "text": user_input,
        "chat_id": chat_id
    }

    try:
        # Send POST request to your webhook endpoint
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            update.message.reply_text("Processing your request...")
        else:
            update.message.reply_text("There was an error processing your request.")
    except Exception as e:
        logger.error("Error connecting to webhook: %s", e)
        update.message.reply_text("Error connecting to processing server.")

def main():
    # Initialize the Telegram bot updater and dispatcher
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Define handlers for commands and messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    # Start the bot by polling Telegram for new messages
    updater.start_polling()
    updater.idle()

if _name_ == '_main_':
    main()