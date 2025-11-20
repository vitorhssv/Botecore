import logging
import random
import sqlite3
from pathlib import Path


def set_logger(module_name: str) -> logging.Logger:
    """Sets a logger"""
    return logging.getLogger(module_name)


logger = set_logger("main_utils")


def get_message(identifier: str, get_random: bool = False) -> str | None:
    """Gets a message from the database.\n\nWhen `get_random is False` the `identifier is message_id`.\n\nWhen `get_random is True` the `identifier is command_id`."""
    try:
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Connected to database")
        cursor = conn.cursor()

        if get_random is False:
            # gets a message using the message_id
            cursor.execute(
                "SELECT message FROM messages WHERE message_id = ?", (identifier,)
            )

            logger.info(f"Message from {identifier} fetched")
            result = cursor.fetchone()[0]
        elif get_random is True:
            # gets a random message using the command_id
            cursor.execute(
                "SELECT message FROM messages WHERE command_id = ?", (identifier,)
            )
            result = random.choice(cursor.fetchall())[0]
            logger.info(f"Messages from {identifier} fetched")

        return result

    except sqlite3.Error as e:
        # log error
        logger.error(e)

    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")


def get_handlers() -> dict[str, str] | None:
    """Gets all handlers from the database in a dict with the command_id"""
    try:
        conn = sqlite3.connect(Path("botConfig.db"))
        logger.info("Connected to database")
        cursor = conn.cursor()

        # gets the handler
        cursor.execute("SELECT command_id, command_handler FROM commands")

        handlers = cursor.fetchall()
        handlers_dict: dict[str, str] = {}
        for handler in handlers:
            new_handler = {f"{handler[0]}": f"{handler[1]}"}
            handlers_dict.update(new_handler)

        return handlers_dict

    except sqlite3.Error as e:
        # log error
        logger.error(e)

    finally:
        # close connection with the database
        if "conn" in locals() and conn:
            conn.close()
            logger.info("Connection closed")
