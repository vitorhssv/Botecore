import sqlite3
from os import execv
from pathlib import Path
from sys import argv, executable

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import *

logger = set_logger("coreFunctions")


# basic "hard-coded" commands, these commands should'nt be deleted or disabled...
async def coreFunctions_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send an introduction to the bot"""
    await update.message.reply_html(get_message("coreFunctions_start_message"))


async def coreFunctions_restart(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Restarts the bot to apply any changes"""
    try:
        await update.message.reply_html(get_message("coreFunctions_restarting_message"))
        execv(executable, ["python"] + argv)
    except (IndexError, ValueError) as e:
        await update.message.reply_html(
            get_message("coreFunctions_restartError_message")
        )
        logger.error(e)


handlers = get_handlers()
coreFunctions_start_handler = CommandHandler(
    handlers["coreFunctions_start"], coreFunctions_start
)
coreFunctions_restart_handler = CommandHandler(
    handlers["coreFunctions_restart"], coreFunctions_restart
)
