import pathlib
from typing import List
import datetime
from zoneinfo import ZoneInfo

import discord
import git
from discord import app_commands
from discord.ext import commands, tasks
from git.repo.base import Repo



class Codeforce(commands.Cog):
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
            "codeforce_invoked": 0,
        }

    @tasks.loop(hours=24)
    async def daily_report(self):
        # Log the daily report
        self.logger.info("Daily Report(codeforce):")
        self.logger.info(f"Number of repo pulls: {self.command_usage_stats['pulls']}")
        self.logger.info(f"Number of codeforce command invocations: {self.command_usage_stats['codeforce_invoked']}")

    @tasks.loop(hours=24)
    async def pull_repo(self):
            o = self.repo.remotes.origin
            o.pull()
            self.logger.info("pulled repo on timer")
            self.command_usage_stats["pulls"] += 1  # Increment pull count


    async def cog_load(self) -> None:
        self.codeforce = pathlib.Path("Codeforces")
        self.codeforce.mkdir(exist_ok=True)
        try:
            self.repo = Repo.clone_from(
                "https://github.com/Waqar-107/Codeforces.git", self.codeforce
            )
            self.logger.info("cloned repo")
            self.repo = Repo(self.codeforce)
        except git.exc.GitCommandError:
            self.repo = Repo(self.codeforce)
            o = self.repo.remotes.origin
            o.pull()
            self.logger.info("pulled repo")

        self.sets = [
            x.name
            for x in self.codeforce.iterdir()
            if x.is_dir() and not x.name.startswith(".")
        ]

    @commands.command()
    async def codeforce(
        self, ctx: commands.Context, number: int, set: str="ACMSGURU"
    ):
        self.command_usage_stats["codeforce_invoked"] += 1
        number = "{:04d}".format(number)
        """Returns the codeforce solution"""
        files = list(self.codeforce.glob( set + "/"+str(number) +"-*" ))
        if set not in self.sets or len(files) == 0:
            await ctx.send(
                f"there are no solutions for codeforce problem #{number} in set-{set}"
            )
            self.logger.info(
                f"{ctx.author} asked for problem #{number} in set-{set} but none exist"
            )
            return
        
        self.logger.info(f"{ctx.author} asked for problem #{number} in set-{set}")
        with open(files[0]) as f:
            code = f.read()
        if ctx.channel.id in self.bot_spam_channels or ctx.channel.name.lower() == "codeforce":
            problem_name = pathlib.Path(files[0].stem).name.replace("-", " ")
            await ctx.send(
                f"Problem #{problem_name} ({set})\n```{set}\n{code}\n```"
            )
        else:
            await ctx.send(f"```{set}\n{code}\n```")




async def setup(bot):
    await bot.add_cog(Codeforce(bot))