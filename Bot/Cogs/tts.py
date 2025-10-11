import asyncio

from discord.ext import commands
from Modules.database_manager import DatabaseManager
from Modules.command_permissions import moderator


class tts(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
