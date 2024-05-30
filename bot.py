import platform
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from helpers.logger import setup_logger

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Logging setup
discord_logger = setup_logger('discord', 'discord.log', level=logging.DEBUG)
server_logger = setup_logger('server', 'server.log')
chat_logger = setup_logger('chat', 'chats.log')

class Vexel(commands.Bot):
    def __init__(self):
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
                self.logger.info(f"Successfully loaded the {filename} cog!")

bot = Vexel(
    command_prefix=commands.when_mentioned_or("!"), # The prefix for commands
    case_insensitive=True, # Whether the commands are case insensitive
    intents=intents, # The intents for the bot to receive events
    help_command=None, # Disable the default help command
    activity=discord.Activity(type=discord.ActivityType.listening, name="!help"), # The activity for the bot to display
    status=discord.Status.idle # The status for the bot to display
  )

# Run bot
bot.run(DISCORD_BOT_TOKEN, log_handler=discord_logger)