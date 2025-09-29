from Modules.reloadable import ReloadableComponent
from Modules.enableable import Enableable
from discord.ext.commands import Cog, Bot


class BaseMischief(Enableable, ReloadableComponent):
    mischief_name = None
    mischief_description = None
    _bot: Bot = None
    
    def __init__(self, bot):
        self._bot = bot
    
    def _set_bot(self, bot):
        if self._bot is None:
            self._bot = bot


class TextMischief(BaseMischief):
    def check(self, normalized_text, message):
        """Check the conditions for the text mischief, must return bool and can be async"""
        raise NotImplementedError
    
    def execute(self, normalized_text, message):
        """Executes the text mischief, can be async"""
        raise NotImplementedError
    
    async def _validate(self, normalized_text, message):
        return self.is_enable and await self._async_dispatch_func(self.check, normalized_text, message)


class CogMischief(BaseMischief, Cog):
    pass