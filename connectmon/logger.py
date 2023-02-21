from connectmon.config import settings

import logging

logger = logging.getLogger("connectmon")

logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """Get a child logger for the given name

    Args:
        name (str): The name of the child logger

    Returns:
        logging.Logger: The child logger
    """
    return logger.getChild(name)
