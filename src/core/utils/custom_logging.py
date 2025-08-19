import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(is_debug: bool = False):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.DEBUG if is_debug else logging.INFO)

    # remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[
        {
            "sink": sys.stdout, "serialize": False, "level": "DEBUG" if is_debug else "INFO",
        },
        {
            "sink": "logs/app.log", "rotation": "5 MB", "retention": "7 days",
            "compression": "zip", "backtrace": True, "diagnose": True,
            "level": "DEBUG" if is_debug else "INFO",
        },
    ])
