from typing import Any
from discord.ext.commands import Bot
from discord import app_commands

from Modules.database_manager import DatabaseManager

class BotClient(Bot):
    def __init__(self, command_prefix, *, help_command = ..., tree_cls = app_commands.CommandTree, description = None, allowed_contexts = ..., allowed_installs = ..., intents, **options):
        super().__init__(command_prefix, help_command=help_command, tree_cls=tree_cls, description=description, allowed_contexts=allowed_contexts, allowed_installs=allowed_installs, intents=intents, **options)
    
    async def load_extensions(self, *names, package: Any = None):
        for name in names:
            await self.load_extension(name, package=package)
    
    async def setup_hook(self):
        await self.load_extension('startup')
        await self.load_extension('Cogs.developer_exclusive')
        
        #await bot.load_extension('Modules.command_manipulation.shared_command_system')
        #await bot.load_extension('Cogs.test')
        
        await self.load_extensions(
            'Cogs.general_commands',
            'Cogs.general_events',
            'Cogs.voice_channel',
            'Cogs.community_notepad',
            'Cogs.youtube_playback.youtube_playback',
            'Cogs.text_channel_selection',
            'Cogs.mass_message_deletion',
            'Cogs.role_tag_controller'
        )
    
    
    async def close(self):
        print("Disconnecting Database...")
        await DatabaseManager.disconnect()
        print("Database Disconnected")
        
        print("Shutting down...")
        return await super().close()