import asyncio, discord

from discord.ext import commands
from Modules.command_manipulation.command_extension import command_extension
from Modules.command_permissions import role_blacklisted
from Modules.Logging.logger import logger

class VoiceChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ping_list = set()
    
    
    async def cog_load(self):
        logger.info(f"Cog Loaded: {self.__cog_name__}")
    
    
    @commands.command("joinCall", aliases = ["entra"])
    @command_extension("ai", "ae")
    @role_blacklisted("forbid_audio_playback", "forbid_voice_chat_control",
        rejection_message="Tu tá BANIDO de mandar o bot coisar na call")
    async def joinCall(self, ctx: commands.Context):
        if ctx.author.voice is not None and hasattr(ctx.author.voice, 'channel'):
            await ctx.reply("ok <:cat:1264072257433632789>")
            await ctx.author.voice.channel.connect()
        else:
            await ctx.reply("Tenta entrar na call primeiro")
    
    
    @commands.command("leaveCall", aliases = ["vaza", "sai"])
    @role_blacklisted("forbid_audio_playback", "forbid_voice_chat_control",
        rejection_message="Tu tá BANIDO de mandar o bot coisar na call")
    async def leaveCall(self, ctx: commands.Context):
        current_call = ctx.voice_client
        
        if current_call:
            await current_call.disconnect()
            await ctx.reply("ok <:cat:1264072257433632789>")
        else:
            await ctx.reply("Eu nem to em call uai")
    
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceChatCommands(bot))