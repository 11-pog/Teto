from discord.ext import commands
from Modules.command_manipulation.shared_command_system import SharedCommand
from Modules.Logging.logger import logger

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    async def cog_load(self):
        logger.info(f"Cog Loaded: {self.__cog_name__}")
    
    
    @SharedCommand.dispatch(full_name = "elabore o horario atual do dia")
    async def pedro(self, ctx):
        pass
    
    
    @commands.group(name = 'jonas')
    async def jonas(self, ctx):
        pass
    
    @jonas.group(name = 'third')
    async def third(self, ctx):
        print("real")
    
    @third.command(name='real')
    async def real(self, ctx):
        print("very")
    
    @third.command(name='unreal')
    async def unreal(self, ctx):
        print("not")
    
    @jonas.command(name = 'first')
    async def jonasthefirste(self, ctx):
        print("BIGGIER CHESSE")
    
    
    @jonas.command(name = 'second')
    async def jonastheseconde(self, ctx):
        print("even BIGGIER CHESSE")





async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot))