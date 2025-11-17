import logging


def set_logger(module_name: str) -> logging.Logger:
    """Sets a logger"""
    return logging.getLogger(module_name)


logger = set_logger("mainUtils")
