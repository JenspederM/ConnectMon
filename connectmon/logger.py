from connectmon.config import settings

import logging

logger = logging.getLogger("connectmon")

logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    return logger.getChild(name)
