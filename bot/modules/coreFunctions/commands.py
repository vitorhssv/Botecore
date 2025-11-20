from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import *


# basic "hard-coded" commands, these commands can't be disabled
async def coreFunctions_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send an introduction to the bot"""
    await update.message.reply_html(get_message("coreFunctions_start_message"))


handlers = get_handlers()
print(handlers["coreFunctions_start"])
coreFunctions_start_handler = CommandHandler(
    handlers["coreFunctions_start"], coreFunctions_start
)
