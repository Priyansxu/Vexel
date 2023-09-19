import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands
from text_by_api import get_response
from image_by_api import get_image
import os
import logging
import requests
import io

"""
debug logging
"""
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

"""
load environment variables from .env file
"""
from dotenv import load_dotenv
load_dotenv()

"""
access discord bot token environment variable
"""
DISCORD_BOT_TOKEN = os.getenv("YOUR_DISCORD_BOT_TOKEN")

"""
define bot intents
"""
intents = discord.Intents.default() 
intents.typing = False
intents.presences = False
intents.message_content = True

"""
initialize bot
"""
bot = commands.Bot(command_prefix='!', intents=intents)

"""
button callback class
"""
class DrawButton(ui.Button['DrawView']):
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer() # acknowledge the interaction
        await draw_image(self.view.message)

"""
view class containing button
"""
class DrawView(ui.View):
    def __init__(self, prompt, message):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.add_item(DrawButton(label='Draw'))
        
"""
helper function to create a view
"""
def draw_view(prompt, message):
    return DrawView(prompt=prompt, message=message)

"""
ready message
"""
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    

"""
main function to process message
"""
@bot.event
async def on_message(message):

    if message.content.startswith('!ask'):
        prompt = message.content[5:].strip()
        response = get_response(prompt)
        api_content = response["content"]
        
        if len(api_content) >= 2000:
            await send_paginated_message(message.channel, api_content, prompt, message)
        else:
            view = draw_view(prompt, message)
            await message.reply(api_content, view=view)

    if message.content.startswith('!draw'):
        await draw_image(message)

"""      
split response message if over Discord's 2000 character limit
"""
async def send_paginated_message(channel, text, prompt, message):
    max_chars = 2000
    start = 0

    while start < len(text):
        end = start + max_chars
        if end > len(text):
            end = len(text)

        chunk = text[start:end]
        chunk = chunk.replace('/', '\/')
        chunk = chunk.replace('>', '\>')

        if end >= len(text):
            view = draw_view(prompt, message)
            await channel.send(chunk, view=view)
        else:
            await channel.send(chunk)

        start = end

"""
draw image
"""
async def draw_image(message):
    prompt = message.content[5:].strip()
    response = get_image(prompt)

    if response.startswith("https"):
        img_url = response

    img_response = requests.get(img_url)

    if img_response.status_code == 200:
        img_bytes = img_response.content
        img_file = io.BytesIO(img_bytes)
        await message.reply(file=discord.File(img_file, "output.png"))
        img_file.close()
    else:
        await message.reply("Failed to fetch the image.")

# run bot
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler)
