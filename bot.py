import platform
import logging
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from helpers.logger import setup_logger

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

discord_logger = setup_logger('discord', 'discord.log', level=logging.DEBUG)
server_logger = setup_logger('server', 'server.log')
chat_logger = setup_logger('chat', 'chats.log')

class Vexel(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = discord_logger
        self.server_logger = server_logger
        self.chat_logger = chat_logger
        self.conversation_histories = {}
  
    async def on_ready(self) -> None:
        self.logger.info(f"{self.user} is now online!")
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    
    async def setup_hook(self) -> None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                self.logger.info(f"Successfully loaded the {filename}!")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = Vexel(
    command_prefix=commands.when_mentioned_or("!"),
    case_insensitive=True,
    intents=intents,
    help_command=None,
    activity=discord.Activity(type=discord.ActivityType.listening, name="@vexel"),
    status=discord.Status.idle
)

bot.run(DISCORD_BOT_TOKEN) 