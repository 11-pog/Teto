import nextcord
from nextcord.ext import commands

from resources_path import ResourcesPath

class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.resources = ResourcesPath()
    
    
    @commands.command(name = "repita")
    async def sendMessage(self, ctx, *, message):
        await ctx.send(message)
        await ctx.message.delete()
    
    
    async def getEmojis(self):
        main_server = await self.bot.fetch_guild(1263933229367562251)
        if main_server:
            emojis = main_server.emojis
        return emojis
    
    
    @commands.command(name = "test")
    async def test(self, ctx):
        #emojis = await self.getEmojis()
        #for x in emojis:
        #    print(f"{x}")
        await ctx.author.send(f"<:trol:968658017086242897>")

    # Comando de ser xingado ai que triste
    @commands.command(name = "xingamento", aliases = ["si", "se", "vai"])
    async def pongbop(self, ctx, *, confirm):
        if confirm in ["mata", "mata mlk", "se fude", "si fude", "sifude", "se foder", "sifuder", "si fuder", "pro caralho", "pra merda", "catar coquinho"]:
            await ctx.reply("<:spong_bop:1264260742975197264>")


    @commands.command(name = "autista")
    async def sendImage(self, ctx):
        file = nextcord.File(f"{self.resources('image')}/autismo.jpg", filename="autismo.png")
        await ctx.send(file=file)
        await ctx.message.delete()


# Comando de Ajuda
    @commands.command(name = "ayuda")
    async def test(self, ctx):
        await ctx.author.send(
            """
            Discurpa, mais tamo refazendo saporra de pagina de ajuda, por favor, volte mais tarde.
            """
            )
        await ctx.author.send("<:spong_bop:1264260742975197264>")



def setup(bot):
    bot.add_cog(GeneralCommands(bot))