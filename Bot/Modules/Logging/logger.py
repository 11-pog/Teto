import logging
from Modules.Logging.formatter import DiscordStyleFormatter
from bot_logging import DiscordLogger


logger = DiscordLogger("AutismBOT", logging.INFO, logging.ERROR)
"""Global logger instance"""

_handler = logging.StreamHandler()
_formatter = DiscordStyleFormatter(datefmt='%Y-%m-%d %H:%M:%S')
_handler.setFormatter(_formatter)

logger.addHandler(_handler)
logger.setLevel(logging.DEBUG)