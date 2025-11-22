import re
import sqlite3
from pathlib import Path

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from utils import *

logger = set_logger("coreFunctions:edit_commands")

CHECK_COMMAND, EDIT_HANDLER, EDIT_DESCRIPTION, CHECK_MESSAGE, EDIT_MESSAGE = range(5)


async def edit_commands(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Asks the user to choose a command to edit"""
    try:
        result_message = "<blockquote>"
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT command_id, command_handler FROM commands WHERE 1 ORDER BY command_id ASC;"
        )
        list = cursor.fetchall()

        for command in list:
            result_message += f"\n<code>{command[0]}</code> - {command[1]}"

        result_message += "</blockquote>"
        await update.message.reply_html(get_message("coreFunctions:choose_command"))
        await update.message.reply_html(result_message)

        return CHECK_COMMAND

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def check_chosen_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Cecks the command_id and asks the user to send the new handler"""
    try:
        context.user_data["chosen_command"] = update.message.text
        chosen_command = context.user_data["chosen_command"]

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT command_handler FROM commands WHERE command_id = ?;",
            (chosen_command,),
        )
        command = cursor.fetchone()

        if command is None:
            # the command id doesn't exist
            await update.message.reply_html(
                get_message("coreFunctions:choice_doesnt_exist")
            )
        else:
            await update.message.reply_html(
                get_message("coreFunctions:send_new_handler")
            )
            return EDIT_HANDLER

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def edit_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Update the command handler and asks the user to send the new description"""
    try:
        new_handler = update.message.text
        chosen_command = context.user_data["chosen_command"]

        if len(new_handler) > 32:
            await update.message.reply_html(
                get_message("coreFunctions:handler_too_long")
            )

            await update.message.reply_html(
                get_message("coreFunctions:send_new_handler")
            )
            return EDIT_HANDLER

        invalid_characters = re.findall("[^A-z_]", new_handler)
        if len(invalid_characters) > 0:
            await update.message.reply_html(
                get_message("coreFunctions:invalid_handler")
            )
            return EDIT_HANDLER

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE commands SET command_handler = ? WHERE command_id = ?",
            (new_handler.lower(), chosen_command),
        )

        conn.commit()
        await update.message.reply_html(
            get_message("coreFunctions:send_new_description")
        )

        return EDIT_DESCRIPTION

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def skip_to_edit_description(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Skips the edit_handler function and goes to edit description"""
    await update.message.reply_html(get_message("coreFunctions:skip_step"))
    await update.message.reply_html(get_message("coreFunctions:send_new_description"))
    return EDIT_DESCRIPTION


async def edit_command_description(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Updates the description and asks the user to choose a message to edit"""
    try:
        new_description = update.message.text
        chosen_command = context.user_data["chosen_command"]

        if len(new_description) > 256:
            await update.message.reply_html(
                get_message("coreFunctions:description_too_long")
            )

            await update.message.reply_html(
                get_message("coreFunctions:send_new_description")
            )
            return EDIT_DESCRIPTION

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE commands SET command_description = ? WHERE command_id = ?",
            (new_description, chosen_command),
        )

        conn.commit()
        result_message = "<blockquote>"
        cursor.execute(
            "SELECT message_id FROM messages WHERE command_id = ? ORDER BY message_id ASC;",
            (chosen_command,),
        )
        list = cursor.fetchall()

        for message in list:
            result_message += f"\n<code>{message[0]}</code>"

        result_message += "</blockquote>"
        await update.message.reply_html(get_message("coreFunctions:choose_message"))
        await update.message.reply_html(result_message)

        return CHECK_MESSAGE

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def skip_to_choose_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Asks the user which message they want to edit"""
    try:
        chosen_command = context.user_data["chosen_command"]
        result_message = "<blockquote>"
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT message_id FROM messages WHERE command_id = ? ORDER BY message_id ASC;",
            (chosen_command,),
        )
        list = cursor.fetchall()

        for message in list:
            result_message += f"\n<code>{message[0]}</code>"

        result_message += "</blockquote>"
        await update.message.reply_html(get_message("coreFunctions:choose_message"))
        await update.message.reply_html(result_message)

        return CHECK_MESSAGE

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def check_chosen_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Cecks the command_id and asks the user to send the new handler"""
    try:
        context.user_data["chosen_message"] = update.message.text
        chosen_message = context.user_data["chosen_message"]

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT message FROM messages WHERE message_id = ?;",
            (chosen_message,),
        )
        message = cursor.fetchone()

        if message is None:
            # the message id doesn't exist
            await update.message.reply_html(
                get_message("coreFunctions:choice_doesnt_exist")
            )
        else:
            await update.message.reply_html(f"<blockquote>{message[0]}</blockquote>")
            await update.message.reply_html(
                get_message("coreFunctions:send_new_message")
            )
            return EDIT_MESSAGE

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def edit_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int | None:
    """Update the command handler and asks the user to send the new description"""
    try:
        new_message = update.message.text
        chosen_message = context.user_data["chosen_message"]
        chosen_command = context.user_data["chosen_command"]

        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE messages SET message = ? WHERE message_id = ?",
            (new_message, chosen_message),
        )

        conn.commit()

        result_message = "<blockquote>"
        cursor.execute(
            "SELECT message_id FROM messages WHERE command_id = ? ORDER BY message_id ASC;",
            (chosen_command,),
        )
        list = cursor.fetchall()

        for message in list:
            result_message += f"\n<code>{message[0]}</code>"

        result_message += "</blockquote>"
        await update.message.reply_html(get_message("coreFunctions:choose_message"))
        await update.message.reply_html(result_message)

        return CHECK_MESSAGE

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """Ends editing the messages"""
    try:
        del context.user_data["chosen_command"]
    except KeyError:
        # the ["chosen_command"] doesn't exist
        pass

    try:
        del context.user_data["chosen_message"]
    except KeyError:
        # the ["chosen_message"] doesn't exist
        pass

    await update.message.reply_html(get_message("coreFunctions:edit_finished"))
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Quits every action"""
    try:
        del context.user_data["chosen_command"]
    except KeyError:
        # the ["chosen_command"] doesn't exist
        pass

    try:
        del context.user_data["chosen_message"]
    except KeyError:
        # the ["chosen_message"] doesn't exist
        pass

    await update.message.reply_html(get_message("coreFunctions:cancel"))
    return ConversationHandler.END


handlers = get_handlers()
edit_commands_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            handlers["coreFunctions:edit_commands"], edit_commands, filters=owner_only
        )
    ],
    states={
        CHECK_COMMAND: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, check_chosen_command),
        ],
        EDIT_HANDLER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_command_handler),
            CommandHandler(handlers["coreFunctions:skip"], skip_to_edit_description),
        ],
        EDIT_DESCRIPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_command_description),
            CommandHandler(handlers["coreFunctions:skip"], skip_to_choose_message),
        ],
        CHECK_MESSAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, check_chosen_message),
            CommandHandler(handlers["coreFunctions:skip"], finish),
        ],
        EDIT_MESSAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_message),
            CommandHandler(handlers["coreFunctions:skip"], finish),
        ],
    },
    fallbacks=[CommandHandler(handlers["coreFunctions:cancel"], cancel)],
)
