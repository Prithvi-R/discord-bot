import os
import logging
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from discord import member
from discord.ext.commands import has_permissions,MissingPermissions
from apikeys import *



class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.client_id = None

        super().__init__(
            command_prefix=commands.when_mentioned_or("?"),
            intents=intents,
            activity=discord.Game(name="💻"),
        )

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------------------------------------------------------------------")
        self.client_id = self.user.id
        try:
            synced = await bot.tree.sync()
            self.logger.info("Synced %s commands", len(synced))
        except Exception as e:
            self.logger.info(e)

    async def setup_hook(self) -> None:
        # Load cogs
        for file in os.listdir(f"./og"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await bot.load_extension(f"og.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    self.logger.exception(f"Failed to load extension {extension}")

    



class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
## File handler
file_handler = RotatingFileHandler(
    filename="bot.log",
    encoding="utf-8",
    mode="a",
    maxBytes=1024 * 1024,
    backupCount=5,
)
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)


# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

bot = Bot()
bot.logger = logger

@bot.tree.command(name="help", description="Displays the help menu")
async def help(interaction: discord.Interaction):
        embed = discord.Embed(title="nuttyBOt Help",
                              color=discord.Color.blue())
        embed.add_field(
            name="Searching for a Leetcode Question",
            value="Use `?leetsearch {ques_detail}` to search for you question.",
            inline=False)
        embed.add_field(
            name="Getting Answer of the LeetCode Question in any Language",
            value="Use `?leetcode {ques_detail} {language}` to get your LeetCode solution.",
            inline=False)
        embed.add_field(
            name="Getting Answer of the CodeForce Question",
            value="Use `?codeforce {ques_no} {ques_set}` to get your Codeforce solution in cpp.",
            inline=False)
        embed.add_field(
            name="Random Questions",
            value="Use ?random to get a random question.",
            inline=False)
        embed.add_field(
            name="Daily Questions",
            value="Use ?daily to get a question of the day.",
            inline=False)
        embed.add_field(
            name="Greeting",
            value="Use `?hello {user}` to Ping.",
            inline=False)

        await interaction.response.send_message(embed=embed)


bot.run(BOTAPI)
