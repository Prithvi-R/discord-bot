import pathlib
from typing import List
import datetime
from zoneinfo import ZoneInfo

from discord import member
from discord.ext.commands import has_permissions,MissingPermissions
import discord
import git
from discord import app_commands
from discord.ext import commands, tasks
from git.repo.base import Repo



class Neetcode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = self.bot.logger
        self.pull_repo.start()
        self.daily_report.start()  # Start the daily report loop
        self.bot_spam_channels = [
            1235254448587280494
        ]
        
        self.command_usage_stats = {
            "pulls": 0,
            "leetcode_invoked": 0,
        }

    @tasks.loop(hours=24)
    async def daily_report(self):
        # Log the daily report
        self.logger.info("Daily Report(leetcode):")
        self.logger.info(f"Number of repo pulls: {self.command_usage_stats['pulls']}")
        self.logger.info(f"Number of leetcode command invocations: {self.command_usage_stats['leetcode_invoked']}")

    @tasks.loop(hours=24)
    async def pull_repo(self):
            o = self.repo.remotes.origin
            o.pull()
            self.logger.info("pulled repo on timer")
            self.command_usage_stats["pulls"] += 1  # Increment pull count


    async def cog_load(self) -> None:
        self.neetcode = pathlib.Path("leetcode")
        self.neetcode.mkdir(exist_ok=True)
        try:
            self.repo = Repo.clone_from(
                "https://github.com/neetcode-gh/leetcode.git", self.neetcode
            )
            self.logger.info("cloned repo")
            self.repo = Repo(self.neetcode)
        except git.exc.GitCommandError:
            self.repo = Repo(self.neetcode)
            o = self.repo.remotes.origin
            o.pull()
            self.logger.info("pulled repo")

        self.languages = [
            x.name
            for x in self.neetcode.iterdir()
            if x.is_dir() and not x.name.startswith(".")
        ]

    # @commands.describe(
    #     number="the number leetcode problem you want a solution for",
    #     language="the coding language",
    # )
    @commands.command()
    async def leetcode(
        self, ctx: commands.Context, number: int, language: str="c"
    ):
        self.command_usage_stats["leetcode_invoked"] += 1
        # add leading zeros to match file names
        number = "{:04d}".format(number)
        """Returns the leetcode solution"""
        files = list(self.neetcode.glob(language + "/" + str(number) + "-*"))
        if language not in self.languages or len(files) == 0:
            await ctx.send(
                f"there are no solutions for leetcode problem #{number} in {language}"
            )
            self.logger.info(
                f"{ctx.author} asked for problem #{number} in {language} but none exist"
            )
            return

        self.logger.info(f"{ctx.author} asked for problem #{number} in {language}")
        with open(files[0]) as f:
            code = f.read()
        if ctx.channel.id in self.bot_spam_channels or ctx.channel.name.lower() == "leetcode":
            problem_name = pathlib.Path(files[0].stem).name.replace("-", " ")
            await ctx.send(
                f"Problem #{problem_name} ({language})\n```{language}\n{code}\n```"
            )
        else:
            await ctx.send(f"```{language}\n{code}\n```")

    # @commands.command()
    # async def hello(self,ctx: commands.Context):
    #     user = ctx.author
    #     channel = ctx.channel
    #     guild = ctx.guild
    #     await ctx.send(f"Hello, {user.mention}! Welcome to {channel.mention} in the server {guild.name}")
    
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



    @commands.command(hidden=True)
    @commands.is_owner()
    async def stats(self, ctx):
        """Reports the usage stats of the bot."""
        stats_message = "Command Usage Stats:\n"
        stats_message += f"Number of repo pulls: {self.command_usage_stats['pulls']}\n"
        stats_message += f"Number of leetcode command invocations: {self.command_usage_stats['leetcode_invoked']}\n"
        
        await ctx.send(stats_message)



async def setup(bot):
    await bot.add_cog(Neetcode(bot))