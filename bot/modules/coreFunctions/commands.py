import sqlite3
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    Bot,
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    Update,
    error,
)
from telegram.ext import CommandHandler, ContextTypes
from utils import *

from .functions import restart_and_update

load_dotenv(override=True)
logger = set_logger("coreFunctions:commands")


# basic "hard-coded" commands, these commands should'nt be deleted or disabled...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an introduction to the bot"""
    await update.message.reply_html(get_message("coreFunctions:start_message"))


async def set_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the bot's commands"""
    await update.message.reply_html(get_message("coreFunctions:setting_commands"))
    scopes = [
        "default",
        "ownerOnly",
        "allPrivateChats",
        "allGroupChats",
        "allChatAdministrators",
    ]
    try:
        all_scopes = [
            BotCommandScopeAllPrivateChats(),
            BotCommandScopeAllChatAdministrators(),
            BotCommandScopeAllGroupChats(),
            BotCommandScopeChat(environ["OWNER_ID"]),
            BotCommandScopeDefault(),
        ]
        for this_scope in all_scopes:
            await Bot(environ["BOT_TOKEN"]).delete_my_commands(this_scope)

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected/created")
        cursor = conn.cursor()

        # adds the commands from the database to the commands_list
        for scope in scopes:
            cursor.execute(
                "SELECT command_handler, command_description FROM commands WHERE command_scope = ?",
                (scope,),
            )
            commands_info = cursor.fetchall()
            commands_list = []

            if scope == "ownerOnly":
                command_scope = BotCommandScopeChat(environ["OWNER_ID"])
            elif scope == "default":
                command_scope = BotCommandScopeDefault()
            elif scope == "allPrivateChats":
                command_scope = BotCommandScopeAllPrivateChats()
            elif scope == "allGroupChats":
                command_scope = BotCommandScopeAllGroupChats()
            elif scope == "allChatAdministrators":
                command_scope = BotCommandScopeAllChatAdministrators()

            if len(commands_info) == 0:
                # if there's no commands with this scope skips to the next one
                continue

            for command_info in commands_info:
                # adds the commands to the commands_list
                commands_list.extend(
                    [
                        BotCommand(
                            command_info[0],
                            command_info[1],
                        )
                    ]
                )

            # adds the commands list to the bot
            await Bot(environ["BOT_TOKEN"]).set_my_commands(
                commands=commands_list, scope=command_scope
            )
            logger.info(f"Commands with {scope} scope added to the commands list")
    except (sqlite3.Error, error.BadRequest) as e:
        # log error
        logger.error(e)
        await update.message.reply_html(
            get_message("coreFunctions:set_commands_error_message")
        )
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")
        await update.message.reply_html(
            get_message("coreFunctions:set_commands_complete")
        )


async def reset_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes every command-related entry from the database"""
    cached_reset_message = get_message("coreFunctions:reset_commands_message")

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
            get_message("coreFunctions:reset_commands_error_message")
        )
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")
        if not restart_and_update():
            await update.message.reply_html(
                get_message("coreFunctions:restart_error_message")
            )


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Restarts the bot to apply any changes"""
    await update.message.reply_html(get_message("coreFunctions:restarting_message"))
    if not restart_and_update():
        await update.message.reply_html(
            get_message("coreFunctions:restart_error_message")
        )


handlers = get_handlers()
start_handler = CommandHandler(
    handlers["coreFunctions:start"], start, filters=authorized_only
)
set_commands_handler = CommandHandler(
    handlers["coreFunctions:set_commands"], set_commands, filters=owner_only
)
reset_commands_handler = CommandHandler(
    handlers["coreFunctions:reset_commands"], reset_commands, filters=owner_only
)
restart_handler = CommandHandler(
    handlers["coreFunctions:restart"], restart, filters=owner_only
)
