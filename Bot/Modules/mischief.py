# mischief.py

import json
from Modules.settings import Settings
from Modules.Logging.logger import logger
import os, random, discord, asyncio, resources_path
from typing import Dict, List

from discord.ext.commands import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Modules.utils import Utils
from Modules.information_manager import InformationManager


REGULAR_AUDIO_PATH: str = os.path.join(resources_path.AUDIOS, "Regular")
RARE_AUDIO_PATH: str = os.path.join(resources_path.AUDIOS, "Rare")
JSON_CHANCE_PATH: str = os.path.join(RARE_AUDIO_PATH, "rare_chances.json")


class Mischief:
    """A considerably small amount of mischief will be caused.
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.info_manager = InformationManager(self.bot)
        
        self.settings = Settings("mischief")
        self.settings.setup(default_structure=
            {
                "guilds":
                    [
                        "Whatsapp 2",
                        "Bot Testing Ground",
                        "VILA DO CHAVES"
                    ],
                "chance_percentage": 1,
                "interval_seconds": 10
            }
        )
        
        if not os.path.exists(JSON_CHANCE_PATH):
            Mischief.create_chance_dict()
        
        self.interval: int = self.settings["interval_seconds"]
        
        self.scheduler_jobs_dict = {}
        self.scheduler = AsyncIOScheduler()
    
    
    async def commence_moderate_mischief(self):
        """STARTS THE FUN
        """
        logger.info('Mischief: Initialized the funny lmao xdxd')
        await self.setup()
        
        self.scheduler_jobs_dict['theTrollingJob'] = self.scheduler.add_job(self.mischief_interface, 'interval', seconds = self.interval)
        self.scheduler.start()
    
    
    async def setup(self):
        guilds: List[discord.Guild] = []
        
        for guild in self.settings["guilds"]:
            found_server = await self.info_manager.fetch_guild_by_name(guild)
            
            if found_server is not None:
                guilds.append(found_server)
        
        self.guilds = guilds
        
        self.regular_audios = os.listdir(REGULAR_AUDIO_PATH)
        self.rare_audios = [path for path in os.listdir(RARE_AUDIO_PATH) if not path.endswith(".json")]
        
        with open(JSON_CHANCE_PATH, 'r') as f:
            self.chances = json.load(f)
    
    
    @staticmethod
    def create_chance_dict():
        with open(JSON_CHANCE_PATH, 'x') as f:
            default_structure = {
                "rare_chance_percentage": 5,
                
                "default_generated_chance": 10,
                "individual_audio_chance": {
                } 
            }
            json.dump(default_structure, f, indent=4)
    
    
    async def QUIT_HAVING_FUN(self):
        """ends the fun D:"""
        self.scheduler.remove_all_jobs()
    
    
    async def mischief_interface(self):
        try:
            if random.uniform(0, 100) <= self.settings["chance_percentage"]:
                await self.perform_a_minuscule_amount_of_despicable_actions()
        except Exception as e:
            await self.on_error(e)
    
    
    async def on_error(self, error: Exception):
        if Utils.has_terminal():
            raise error
        
        dev = await self.info_manager.get_bot_dev()
        
        if dev:
            await dev.send(f'Error in MISCHIEF:\n{error}')
    
    
    async def get_populated_vcs(self) -> List[discord.VoiceChannel]:
        voice_channels = []
        
        for guild in self.guilds:
            if not any(VcClients.guild.id == guild.id for VcClients in self.bot.voice_clients):
                voice_channels += guild.voice_channels
        
        return [voice_channel for voice_channel in voice_channels if len(voice_channel.voice_states) > 0]
    
    
    async def updt_json(self):
        with open(JSON_CHANCE_PATH, 'w') as f:
            json.dump(self.chances, f)
    
    
    async def fill_json_default_songs(self):
        song_chances: Dict[str, int] = self.chances["individual_audio_chance"]
        default_chance = self.chances["default_generated_chance"]
        
        for filename in self.rare_audios:
            song_chances.setdefault(filename, default_chance)
        
        self.chances["individual_audio_chance"] = song_chances
        await self.updt_json
    
    
    async def get_rare_audio(self):
        pass
    
    async def get_regular_audio(self):
        selected_audio: str = random.choice(self.regular_audios)
        audio_path: str = os.path.join(REGULAR_AUDIO_PATH, selected_audio)
        
        return audio_path, selected_audio
    
    
    async def get_random_audio(self):
        if random.uniform(0, 100) <= self.chances["rare_chance_percentage"]:
            audio_path, name = await self.get_rare_audio()
        else:
            audio_path, name = await self.get_regular_audio()
        
        return audio_path, name
    
    
    async def perform_a_minuscule_amount_of_despicable_actions(self):
        voice_channels = await self.get_populated_vcs()
        
        if len(voice_channels) == 0:
            logger.debug('Mischief: No voice channels available')
            return
        
        await random.choice(voice_channels).connect()
        
        audio_path, audio_name = await self.get_random_audio()
        source = discord.FFmpegPCMAudio(audio_path)
        
        vc_bot_client = self.bot.voice_clients[0]
        
        await asyncio.sleep(random.randint(1, 10))
        
        flag = asyncio.Event()
        
        def stop(err):
            if err:
                print(err)
            flag.set()
        
        vc_bot_client.play(source, after = stop)
        logger.info(f"Mischief: Love me some {audio_name}")
        
        await flag.wait()
        
        await asyncio.sleep(random.uniform(0, 0.2))  
        await vc_bot_client.disconnect()


if __name__ == "__main__":
    bot = Bot('test')
    loki = Mischief(bot)
    
    auauaudio = asyncio.run(loki.get_random_audio())
    pass