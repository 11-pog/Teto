import traceback
from typing import Any

import discord
from discord.ext.commands import Bot, Context
from discord import app_commands

from Modules.information_manager import InformationManager
from Modules.database_manager import DatabaseManager

class BotClient(Bot):
    def __init__(self, command_prefix, *, help_command = ..., tree_cls = app_commands.CommandTree, description = None, allowed_contexts = ..., allowed_installs = ..., intents, **options):
        super().__init__(command_prefix, help_command=help_command, tree_cls=tree_cls, description=description, allowed_contexts=allowed_contexts, allowed_installs=allowed_installs, intents=intents, **options)
        
        self.info_manager = InformationManager(self)
        
        self.dev_user = None
        self.dev_dm_as_err_output = False
    
    def set_error_output_as_dev(self, state: bool):
        self.dev_dm_as_err_output = True
    
    async def load_extensions(self, *names, package: Any = None):
        for name in names:
            await self.load_extension(name, package=package)
    
    async def setup_hook(self):
        self.dev_user = await self.info_manager.get_bot_dev()
        
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
    
    
    async def on_command_error(self, context: Context, exception: Exception):
        if self.dev_dm_as_err_output:
            await self._report_error_dm(context, exception)
        
        return await super().on_command_error(context, exception)
    
    
    async def _report_error_dm(self, context: Context, exception: Exception):
        error_type = exception.__class__.__name__
        if error_type == "CommandNotFound":
            return
        
        embed = discord.Embed(
            title="Error Caught",
            description=f"An error occurred in `{context.guild.name}`",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Server", value=f"`{context.guild.name}` (ID: `{context.guild.id}`)", inline=False)
        embed.add_field(name="Channel", value=f"<#{context.channel.id}> (`{context.channel.id}`)", inline=False)
        embed.add_field(name="Invoker", value=f"{context.author} (ID: `{context.author.id}`)", inline=False)
        embed.add_field(name="Command", value=f"`{context.command}`", inline=False)
        embed.add_field(name="Error Type", value=f"`{error_type}`", inline=True)
        embed.add_field(name="Error Message", value=f"`{exception}`", inline=True)
        embed.add_field(name="Message Content", value=f"```plaintext\n{context.message.content}\n```", inline=False)
        
        embed.set_footer(text="Error Logger")
        embed.timestamp = context.message.created_at
        
        await self.dev_user.send(embed=embed)