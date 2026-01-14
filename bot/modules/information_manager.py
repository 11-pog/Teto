# bot_utilities.py

import os, discord

class InformationManager:
    """information related functions for the bot.
    """
    def __init__(self, bot_object: discord.Client):
        """
        Args:
            bot_object (nextcord.Client): The nextcord bot object that represents the bot
        """
        self.bot = bot_object
    
    
    async def get_guild_by_name(self, desired_server_name: str) -> discord.Guild | None:
        """Returns a server object by its name, returns None if no server is found
        
        Args:
            desired_server_name (str): the server name to search for
        
        Returns:
            Guild: the server object if found
            None: if no server is found
        """
        servers = self.bot.guilds
        
        for server in servers:
            if server.name == desired_server_name:
                return server
        
        return None
    
    
    async def fetch_member_by_name(self, member_name: str) -> discord.Member | None:
        """Returns a member object by its name, returns None if no member is found
        
        Args:
            member_name (str): the member name to search for
        
        Returns:
            Member: the member object if found
            None: if no member is found
        """
        servers = self.bot.guilds
        
        for server in servers:
            member_list = await server.fetch_members().flatten()
            
            for member in member_list:
                if member.name == member_name:
                    return member
        
        return None
    
    
    async def get_bot_dev(self):
        bot_developer_id = int(os.environ['BOT_DEV_DISCORD_ID'])
        return await self.bot.fetch_user(bot_developer_id)