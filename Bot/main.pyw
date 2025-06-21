# main.py

import os, time

from Modules.utils import Utils
from resources_path import resources_path

NAME = os.path.join(resources_path('lock'), 'AutismBOT_LOCK')
lock = Utils.is_duplicate(NAME)

if lock is None:
    print(f"Process is a duplicate, exiting...")
    time.sleep(1)
    exit()


# Main package import
import discord

from discord import Intents
from bot import BotClient


# Module import
from Modules.database_manager import DatabaseManager
from Modules.command_permissions import is_user_role_tagged


#Bot Instantiation
intents = Intents.default()

intents.message_content = True
intents.members = True

bot = BotClient(command_prefix=['aproveita e '], intents=intents, help_command= None, case_insensitive=True)


@bot.event
async def on_message(msg: discord.Message):
    if msg.content.startswith(tuple(await bot.get_prefix(msg))) and await is_user_role_tagged(await bot.get_context(msg), 'forbid_BOT'):
        print(f'Blacklisted user "{msg.author.name}" tried using bot in {msg.guild.name}, {msg.channel.name}')
        return
    
    await bot.process_commands(msg)


if __name__ == '__main__':
    bot.run(os.environ['AUTISM_DISCORD_TOKEN'])