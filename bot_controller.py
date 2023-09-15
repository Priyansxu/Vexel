import discord
from discord.ext import commands
from text_by_api import get_response
from image_by_api import get_image
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
intents.typing = False  # you can adjust these based on your bot's needs
intents.presences = False
intents.message_content = True  # enable message content intent

# initialize the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user: # ignore messages from the bot itself
        return

    # if the message starts with !ask, send the prompt to the API
    if message.content.startswith('!ask'):
        # get the prompt from the message content
        prompt = message.content[5:].strip()
        # get the response from the API
        response = get_response(prompt)
        # extract only the content message from the API response
        api_content = response["content"]
        if len(api_content) >= 2000:
            await send_paginated_message(message.channel, api_content)
        else:
            # otherwise, send the response as-is
            await message.reply(api_content)

    if message.content.startswith('!draw'):
        prompt = message.content[5:].strip()
        response = get_image(prompt)
        await message.reply(response)
    
# splits response message if over Discord's 2000 character limit
async def send_paginated_message(channel, text):
    max_chars = 2000
    start = 0 # index 0 of text

    # iterate through text in chunks of 2000 characters
    while start < len(text):
        end = start + max_chars # end index of each chunk
        if end > len(text):
            end = len(text)  # prevents out of bounds error

        # escape / and > characters before sending
        chunk = text[start:end]
        chunk = chunk.replace('/', '\/')  # replace / with \/
        chunk = chunk.replace('>', '\>')  # replace > with \>

        if text[end:end + 1] == '\0':  # check for a null character
            await channel.send(chunk)
            return
        else:
            await channel.send(chunk)
            start = end # update start index for next chunk

# run the bot
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler)

