import asyncio, signal

from discord.ext import commands
from Modules.Logging.logger import logger
from Modules.utils import StringTools, Utils
from Modules.information_manager import InformationManager
from Modules.database_manager import DatabaseManager

class GeneralEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = DatabaseManager()
        self.info = InformationManager(self.bot)
    
    async def cog_load(self):
        logger.info(f"Cog Loaded: {self.__cog_name__}")
    
    
    def shutdown_request(self, signal_received, frame):
        self.bot.loop.create_task(DatabaseManager.disconnect_all())
        self.bot.loop.create_task(self.bot.close())
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if str.lower(msg.content) == 'fat fuck' and msg.author.id != self.bot.user.id:
            await msg.channel.send(msg.content)
        
        elif str.lower(msg.content).startswith(tuple(await self.bot.get_prefix(msg))):
            the_big_forbidden_list_of_bad_words = await Utils.get_the_forbidden_list()
            
            if any(bad_word in StringTools.clean(msg.content) for bad_word in the_big_forbidden_list_of_bad_words):
                await msg.reply("<:spong_bop:1264260742975197264>")
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.database.setup(structure={
            'storedLocations': {
                'channel_ID': 'INTEGER',
                'server_ID': 'INTEGER',
                'general_ID': 'INTEGER'
            }
        })
        
        fetch_locations_query = "SELECT channel_ID, server_ID FROM storedLocations WHERE general_ID = 0"
        locations_data = await self.database.fetchall(fetch_locations_query)
        
        for location_record in locations_data:
            marked_server = self.bot.get_guild(location_record[1])
            greetings_channel = self.bot.get_channel(location_record[0])
            
            if greetings_channel:
                await greetings_channel.send("Boa tarde")
                logger.info(f"Message sent to: {marked_server.name}")
            else:
                logger.info(f'Guild "{marked_server.name}" does not have a "Welcome" channel')


async def setup(bot: commands.Bot):
    cog = GeneralEvents(bot)
    
    signal.signal(signal.SIGTERM, cog.shutdown_request)
    signal.signal(signal.SIGINT, cog.shutdown_request)
    
    await bot.add_cog(cog)