import platform
import logging
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

class Vexel(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_histories = {}

    async def on_ready(self) -> None:
        logger.info(f"{self.user.name} is now online.")
        logger.info(f"discord.py API version: {discord.__version__}")
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

    async def setup_hook(self) -> None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Successfully loaded {filename[:-3]} command!")
        await self.tree.sync()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = False

bot = Vexel(
    intents=intents,
    help_command=None,
    activity=discord.Activity(type=discord.ActivityType.listening, name="@vexel"),
    status=discord.Status.idle
)

bot.run(DISCORD_BOT_TOKEN)