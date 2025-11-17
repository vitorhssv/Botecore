import logging
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


def main() -> None:
    """Start the bot"""
    # create the bot and add it's handlers
    application = Application.builder().token(environ["BOT_TOKEN"]).build()
    application.add_handlers(all_handlers)
    # start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
