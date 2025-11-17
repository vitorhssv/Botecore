import logging
import sqlite3
from importlib import import_module
from os import environ, listdir
from pathlib import Path

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

# create a list for default info
all_handlers = []
all_commands_defaults: list[dict[str, str]] = []

# make a list of the installed modules and add all of it's handlers and commands_defaults into another list
modules = listdir(Path("./modules"))
for module in modules:
    imported = import_module(f"modules.{module}")
    all_handlers.extend(imported.handlers)
    all_commands_defaults.extend(imported.commands_defaults)

# database check & setup
try:
    # connect to the database
    conn = sqlite3.connect(Path("config/botConfig.db"))
    logger.info("Database connected/created")
    cursor = conn.cursor()

    # create tables
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS commands (
            command_id TEXT PRIMARY KEY,
            command_handler TEXT UNIQUE,
            scope INT NOT NULL,
            enabled BOOL NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            command_id TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS allowed (
            id INT PRIMARY KEY,
            type TEXT NOT NULL
        );
        """
    )
    logger.info("Tables were created/already exists")
    conn.commit()
except sqlite3.Error as e:
    # log error
    logger.error(e)
finally:
    # close connection with the database
    if "conn" in locals() and conn:
        conn.close()
        logger.info("Connection closed")


def main() -> None:
    """Start the bot"""
    # create the bot and add it's handlers
    application = Application.builder().token(environ["BOT_TOKEN"]).build()
    application.add_handlers(all_handlers)
    # start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
