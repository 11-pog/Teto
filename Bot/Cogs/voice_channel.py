from nextcord.ext import commands

class VoiceChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command("joinCall", aliases = ["entra"])
    async def joinCall(self, ctx, a1):
        if a1 in ["ai", "ae"]:
            if hasattr(ctx.author.voice, 'channel'):
                await ctx.reply("ok <:cat:1264072257433632789>")
                await ctx.author.voice.channel.connect()
            else:
                await ctx.reply("Tenta entrar na call primeiro")

    @commands.command("leaveCall", aliases = ["vaza", "sai"])
    async def leaveCall(self, ctx):
        currentCall = ctx.voice_client
        if currentCall:
            await currentCall.disconnect()
            await ctx.reply("ok <:cat:1264072257433632789>")
        else:
            await ctx.reply("eu nem to em call uai")


def setup(bot):
    bot.add_cog(VoiceChatCommands(bot))