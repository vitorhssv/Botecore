import sqlite3
from pathlib import Path

from telegram import (
    KeyboardButton,
    KeyboardButtonRequestUsers,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from utils import *

logger = set_logger("coreFunctions:manage_permission_list")

ADD_OR_REMOVE, ADD_CONTACTS, REMOVE_CONTACTS = range(3)


def get_allowed_list(count: bool = False) -> str | None:
    try:
        result_message = "<blockquote>"
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM allowed WHERE 1 ORDER BY name ASC;")
        list = cursor.fetchall()

        user_count = 0
        for user in list:
            user_count += 1
            result_message = (
                result_message
                + f"\n{f'{user_count} - ' if count is True else ''}<a href='tg://user?id={user[0]}'>{user[1]}</a>"
            )

        return result_message + "</blockquote>"

    except sqlite3.Error as e:
        # log error
        logger.error(e)
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


async def manage_permission_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Add or remove people who can use the bot"""
    reply_keyboard = [
        [
            get_message("coreFunctions:add_to_list"),
            get_message("coreFunctions:remove_from_list"),
        ]
    ]

    await update.message.reply_html(
        get_message("coreFunctions:add_or_remove_choice"),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
        ),
    )
    try:
        await update.message.reply_html(get_allowed_list())
    except:
        await update.message.reply_html(
            get_message("coreFunctions:allowed_list_is_empty")
        )

    return ADD_OR_REMOVE


async def add_to_list_request(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Request to add a contact to the permission list"""
    await update.message.reply_html(
        get_message("coreFunctions:add_contact_explanation"),
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        get_message("coreFunctions:add_contacts_button"),
                        request_users=KeyboardButtonRequestUsers(
                            request_id=1,
                            user_is_bot=False,
                            request_name=True,
                            max_quantity=10,
                        ),
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    return ADD_CONTACTS


async def add_contacts_to_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Add the contacts to the permission list"""
    users_shared = update.message.users_shared
    if users_shared:
        try:
            conn = sqlite3.connect(Path("botConfig.db"))
            logger.info("Database connected")
            cursor = conn.cursor()

            for user in users_shared.users:
                cursor.execute(
                    "SELECT id FROM allowed WHERE id = ?;",
                    (user.user_id,),
                )
                user_in_db = cursor.fetchone()

                if user_in_db is None:
                    # if the user is not on the database, add them
                    cursor.execute(
                        "INSERT INTO allowed VALUES (?, ?);",
                        (
                            user.user_id,
                            user.name,
                        ),
                    )

            conn.commit()
            await update.message.reply_text(
                get_message("coreFunctions:users_added_successfully")
            )
        except sqlite3.Error as e:
            # log error
            logger.error(e)
            await update.message.reply_text(
                get_message("coreFunctions:error_while_adding_users")
            )
        finally:
            # close connection with the database
            if "conn" in locals() and conn:
                conn.close()
                logger.info("Connection closed")
            try:
                await update.message.reply_html(get_allowed_list())
            except:
                await update.message.reply_html(
                    get_message("coreFunctions:allowed_list_is_empty")
                )
    else:
        # no users sent
        await update.message.reply_text(get_message("coreFunctions:no_users_were_sent"))

    return ConversationHandler.END


async def remove_from_list_request(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Request to remove the contacts from the permission list"""
    await update.message.reply_html(
        get_message("coreFunctions:remove_contact_explanation"),
        reply_markup=ReplyKeyboardRemove(),
    )
    # send the list with number counting each user
    try:
        await update.message.reply_html(get_allowed_list(True))
    except:
        await update.message.reply_html(
            get_message("coreFunctions:allowed_list_is_empty")
        )

    return REMOVE_CONTACTS


async def remove_contacts_from_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Remove contacts from the permission list"""
    try:
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Database connected")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM allowed WHERE 1 ORDER BY name ASC;")
        users_list = cursor.fetchall()

        to_remove_tuple = update.message.text.split(" ")
        to_remove = [item[0] for item in to_remove_tuple]

        for index in to_remove:
            real_index = int(index) - 1
            cursor.execute(
                "DELETE FROM allowed WHERE id = ?",
                (users_list[real_index][0],),
            )

        conn.commit()
    except sqlite3.Error as e:
        # log error
        logger.error(e)
        await update.message.reply_text(
            get_message("coreFunctions:error_while_removing_users")
        )
    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")

        await update.message.reply_text(
            get_message("coreFunctions:users_removed_from_list")
        )
        try:
            await update.message.reply_html(get_allowed_list())
        except:
            await update.message.reply_html(
                get_message("coreFunctions:allowed_list_is_empty")
            )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    await update.message.reply_html(get_message("coreFunctions:cancel"))
    return ConversationHandler.END


handlers = get_handlers()
manage_permission_list_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            handlers["coreFunctions:manage_permission_list"],
            manage_permission_list,
            filters=owner_only,
        )
    ],
    states={
        ADD_OR_REMOVE: [
            MessageHandler(filters.Regex("(?i)^(add)$"), add_to_list_request),
            MessageHandler(filters.Regex("(?i)^(remove)$"), remove_from_list_request),
        ],
        ADD_CONTACTS: [MessageHandler(filters.USER, add_contacts_to_list)],
        REMOVE_CONTACTS: [MessageHandler(filters.TEXT, remove_contacts_from_list)],
    },
    fallbacks=[CommandHandler(handlers["coreFunctions:cancel"], cancel)],
)
