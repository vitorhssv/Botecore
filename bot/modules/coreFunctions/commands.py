import sqlite3
from pathlib import Path

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import *

from .functions import restart

logger = set_logger("coreFunctions")


# basic "hard-coded" commands, these commands should'nt be deleted or disabled...
async def coreFunctions_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send an introduction to the bot"""
    await update.message.reply_html(get_message("coreFunctions_start_message"))


async def coreFunctions_resetCommands(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Deletes every command-related entry from the database"""
    cached_reset_message = get_message("coreFunctions_resetCommands_message")

    try:
        # connect to the database
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected/created")
        cursor = conn.cursor()

        # create tables
        cursor.execute(
            """
            DELETE FROM commands WHERE 1;
            """
        )
        cursor.execute(
            """
            DELETE FROM messages WHERE 1;
            """
        )

        logger.info("Deleted every command-related entry from the database")

        conn.commit()
        await update.message.reply_html(cached_reset_message)

    except sqlite3.Error as e:
        # log error
        logger.error(e)
        await update.message.reply_html(
            get_message("coreFunctions_resetCommandsError_message")
        )
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")
        if not restart():
            await update.message.reply_html(
                get_message("coreFunctions_restartError_message")
            )


async def coreFunctions_restart(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Restarts the bot to apply any changes"""
    await update.message.reply_html(get_message("coreFunctions_restarting_message"))
    if not restart():
        await update.message.reply_html(
            get_message("coreFunctions_restartError_message")
        )


handlers = get_handlers()
coreFunctions_start_handler = CommandHandler(
    handlers["coreFunctions_start"], coreFunctions_start
)
coreFunctions_resetCommands_handler = CommandHandler(
    handlers["coreFunctions_resetCommands"], coreFunctions_resetCommands
)
coreFunctions_restart_handler = CommandHandler(
    handlers["coreFunctions_restart"], coreFunctions_restart
)
