from discord.ext.commands import Bot
from discord import app_commands

class BotClient(Bot):
    def __init__(self, command_prefix, *, help_command = ..., tree_cls = app_commands.CommandTree, description = None, allowed_contexts = ..., allowed_installs = ..., intents, **options):
        super().__init__(command_prefix, help_command=help_command, tree_cls=tree_cls, description=description, allowed_contexts=allowed_contexts, allowed_installs=allowed_installs, intents=intents, **options)
    
    async def setup_hook(self):
        await self.load_extension('startup_cog')
        
        #await bot.load_extension('Modules.command_manipulation.shared_command_system')
        #await bot.load_extension('Cogs.test')
        
        await self.load_extension('Cogs.developer_exclusive')
        await self.load_extension('Cogs.general_commands')
        await self.load_extension('Cogs.general_events')
        await self.load_extension('Cogs.voice_channel')
        await self.load_extension('Cogs.community_notepad')
        await self.load_extension('Cogs.youtube_playback.youtube_playback')
        await self.load_extension('Cogs.text_channel_selection')
        await self.load_extension('Cogs.mass_message_deletion')
        await self.load_extension('Cogs.role_tag_controller')