from connectmon.env import env

import logging

logger = logging.getLogger("connectmon")

logging.basicConfig(format=env.LOG_FORMAT, level=env.LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """Get a child logger for the given name

    Args:
        name (str): The name of the child logger

    Returns:
        logging.Logger: The child logger
    """
    return logger.getChild(name)
