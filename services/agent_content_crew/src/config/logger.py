import logging
import sys
import types

from logging import Formatter, StreamHandler, getLogger

log_format = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

class CustomFormatter(Formatter):
    """Custom formatter to add colors to log levels."""
    
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: "\x1b[36;20m" + log_format + reset,  # Cyan
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, log_format)
        formatter = Formatter(log_fmt, date_format)
        return formatter.format(record)
    
console_handler = StreamHandler(sys.stdout)
console_handler.setFormatter(CustomFormatter())

logger = getLogger("AGENT_CONTENT_CREW")
logger.setLevel(logging.INFO)

def custom_info(self, msg, *args, **kwargs):
    if getattr(self, 'SHOW_FINAL_RESULT', False):
        # If this flag is set, just print the raw message
        print(msg)
        self.SHOW_FINAL_RESULT = False
    else:
        # Otherwise, use the standard log method
        super(type(self), self).info(msg, *args, **kwargs)

logger.info = types.MethodType(custom_info, logger)

# Add the handler to the logger
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.propagate = False # Prevent logs from bubbling up to the root logger