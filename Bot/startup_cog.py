from discord.ext import commands
from Modules.mischief import Mischief
from Modules.database_manager import DatabaseManager
from Modules.command_permissions import Permission

class startup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.fnuuy = Mischief(bot,
            servers_with_tomfoolery_present= [
                "Whatsapp 2",
                "Bot Testing Ground",
                "VILA DO CHAVES"
                ],
            chance_denominator=110,
            interval_in_seconds = 12
            )
    
    
    async def cog_load(self):
        await DatabaseManager.connect()
        print("DatabaseManager: Database has Connected")

        await Permission.database_init()
        print("Permission: Permission database has been Setup")
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot is online! Username: {self.bot.user.name} | ID: {self.bot.user.id}")
        print("Connected to the following guilds:")
        for guild in self.bot.guilds:
            print(f" - {guild.name} (ID: {guild.id})")
        
        await self.fnuuy.commence_moderate_mischief()


async def setup(bot: commands.Bot):
    await bot.add_cog(startup(bot))
