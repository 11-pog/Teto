import asyncio
from nextcord.ext import commands

class MassMessageDeletion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_deletion_dict = {}


    # Pra marcar
    @commands.command(name = "toMark", aliases = ["marca"])
    async def mark(self, ctx):
        channelID = ctx.channel.id
        if channelID not in self.message_deletion_dict:
            self.message_deletion_dict[channelID] = []
            self.message_deletion_dict[channelID].append(ctx.message)
            await ctx.reply("marquei meu")


    # Pra deletar
    @commands.command(name = "toDelete", aliases = ["deleta"])
    async def delete(self, ctx):
        channel_id = ctx.channel.id
        finalMsgsToDel = []

        if channel_id in self.message_deletion_dict:
            messages_to_delete = self.message_deletion_dict[channel_id]

            async def delete_message(msg):
                await msg.delete()

            for items in messages_to_delete:
                try:
                    finalMsgsToDel.append(delete_message(items))
                except:
                    pass

            await asyncio.gather(*finalMsgsToDel)
            del self.message_deletion_dict[channel_id]

            await ctx.author.send("Pronto fi")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.message_deletion_dict:
            self.message_deletion_dict[message.channel.id].append(message)


def setup(bot):
    bot.add_cog(MassMessageDeletion(bot))