import discord
from discord.ext import commands
from text_by_api import get_response
import os
import logging

# debug logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# access the discord bot token environment variable
DISCORD_BOT_TOKEN = os.getenv("YOUR_DISCORD_BOT_TOKEN")

# define the intents for your bot
intents = discord.Intents.default()
intents.typing = False  # You can adjust these based on your bot's needs
intents.presences = False
intents.message_content = True  # Enable message content intent

# initialize the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

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
        # extract only the content message from the API response
        api_content = response["content"]
        if len(api_content) >= 2000:
            await send_paginated_message(message.channel, api_content)
        else:
            # Otherwise, send the response as-is
            await message.reply(api_content)
    
# function to send a paginated message
async def send_paginated_message(channel, text):
    max_chars = 2000  # discord's maximum message length
    start = 0

    while start < len(text):
        end = start + max_chars
        if end > len(text):
            end = len(text)  # ensure end doesn't go beyond the text length

        # escape / and > characters before sending
        chunk = text[start:end]
        chunk = chunk.replace('/', '\/')  # replace / with \/
        chunk = chunk.replace('>', '\>')  # replace > with \>

        if text[end:end + 1] == '\0':  # check for a null character
            await channel.send(chunk)
            return
        else:
            await channel.send(chunk)
            start = end


# run the bot with your Discord bot token
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler)

