import discord
from discord.ext import commands
from text_by_api import get_response
import os

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# access the discord bot token environment variable
DISCORD_BOT_TOKEN = os.getenv("YOUR_DISCORD_BOT_TOKEN")

# initialize the Discord bot
bot = commands.Bot(command_prefix='!')

# OPTIONAL -- define the channel ID where the bot should respond. 
# Otherwise, it will respond to all channels.
# target_channel_id = "YOUR_TARGET_CHANNEL_ID"  # Replace with the actual channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ask'):
        prompt = message.content[5:].strip()
        response = get_response(prompt)
        await message.channel.send(response)

# run the bot with your Discord bot token
bot.run("DISCORD_BOT_TOKEN")

