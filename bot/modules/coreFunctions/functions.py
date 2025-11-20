from os import execv
from sys import argv, executable

from utils import *

logger = set_logger("coreFunctions")


def restart_and_update():
    try:
        # restarts the bot without the -start argument so the database is updated
        execv(executable, ["python"] + argv[:-1])
    except (IndexError, ValueError) as e:
        logger.error(e)
        return False
