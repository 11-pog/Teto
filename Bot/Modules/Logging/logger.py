import logging
from Modules.settings import Settings
from Modules.reloadable import ReloadableComponent
from Modules.Logging.formatter import DiscordStyleFormatter
from Modules.Logging.discord_logger import DiscordLogger, getLevelValue


logger = DiscordLogger("AutismBOT", logging.NOTSET, logging.ERROR)
"""Global logger instance"""

class _logger_set(ReloadableComponent):
    def __init__(self):
        super().__init__()
        
        self.config = Settings("debug")
        self.config.setup(default_structure=
            {
            "log_level": "INFO"
            }
        )
        
        self.load()
    
    def load(self):
        _handler = logging.StreamHandler()
        _formatter = DiscordStyleFormatter(datefmt='%Y-%m-%d %H:%M:%S')
        _handler.setFormatter(_formatter)
        
        logger.addHandler(_handler)
        self.set_level()
    
    def set_level(self):
        log_level_str = self.config.get("log_level")
        log_level_value = getLevelValue(log_level_str)
        logger.setLevel(log_level_value)
        logger.info(f"Set level to {log_level_str}")
    
    def reload(self):
        self.set_level()


_log_config = _logger_set()