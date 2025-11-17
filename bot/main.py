import logging
from os import environ

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application

load_dotenv(override=True)

# logger setup and configuration
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
if environ["LOG_LEVEL"] == "0":
    logging.basicConfig(format=log_format, level=logging.INFO)
else:
    logging.basicConfig(format=log_format, level=logging.WARNING)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("botStartScript")


def main() -> None:
    """Start the bot"""
    # create the bot and add it's handlers
    application = Application.builder().token(environ["BOT_TOKEN"]).build()
    # start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
