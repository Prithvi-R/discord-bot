from discord import member
from discord.ext.commands import has_permissions,MissingPermissions
import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = self.bot.logger
        self.bot_spam_channels = [
            1235254448587280494
        ]
    @commands.command()
    async def hello(self,ctx: commands.Context):
        user = ctx.author
        channel = ctx.channel
        guild = ctx.guild
        await ctx.send(f"Hello, {user.mention}! Welcome to {channel.mention} in the server {guild.name}")
    

    # @commands.Cog.listener()
    # async def on_message(self,message):
    #     # print(f"Author:{message.author} Message content: {message.content}")
    #     # print("")

    #     if "del" in message.content:
    #         try:
    #             await message.delete()   
    #             self.logger.info(f"Deleted_Message - By:{message.author} Message: {message.content}")
    #             await message.channel.send("The removable text has been succefully removed")
    #         except:
    #             self.logger.info(f"Permissions Not Found - By:{message.author} Message: {message.content}")
    #             await message.channel.send("Bot Does't have required permissions")
    #     await self.bot.process_commands(message)




async def setup(bot):
    await bot.add_cog(Basic(bot))