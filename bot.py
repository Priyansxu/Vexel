import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands
from ask import get_response
from draw import get_image
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
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

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
        await draw_image(self.view.api_content, self.view.message)

"""
view class containing button
"""
class DrawView(ui.View):
    def __init__(self, prompt, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.api_content = api_content
        self.add_item(DrawButton(label='Draw'))
        
"""
helper function to create a view
"""
def draw_view(prompt, message, api_content):
    return DrawView(prompt=prompt, message=message, api_content=api_content)

"""
ready message
"""
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="!ask & !draw"))
    print(f'Logged in as {bot.user.name}')

"""
main function to process message
"""
@bot.event
async def on_message(message):
    
    prompt = message.content[5:].strip() # get prompt from message content

    if message.content.startswith('!ask'): # text controller
        response = get_response(prompt) # get response from API
        api_content = response["content"] # extract only content message from API response
        
        if len(api_content) >= 2000: # paginate response if over Discord's character limit
            await send_paginated_message(message.channel, api_content, prompt, message)
        else:
            view = draw_view(prompt, message, api_content)
            await message.reply(api_content, view=view)

    if message.content.startswith('!draw'): # image controller using OpenAI API
        await draw_image(prompt, message)

"""      
split response message if over Discord's 2000 character limit
"""
async def send_paginated_message(channel, api_content, prompt, message):
    max_chars = 2000
    start = 0 # index 0 of text
    text = api_content

    while start < len(text):  # iterate through text in chunks of 2000 characters
        end = start + max_chars # end index of each chunk
        if end > len(text):
            end = len(text) # prevent out of bounds error
        
        chunk = text[start:end] # escape / and > characters before sending
        chunk = chunk.replace('/', '\/') # replace / with \/
        chunk = chunk.replace('>', '\>') # replace > with \>

        if end >= len(text):
            view = draw_view(prompt, message, api_content) # creates Draw button
            await channel.send(chunk, view=view)
        else:
            await channel.send(chunk)

        start = end

"""
draw image
"""
async def draw_image(prompt, message):
    await message.reply("Drawing...") # command acknowledge message
    response = get_image(prompt)

    if response.startswith("https"):
        img_url = response
    img_response = requests.get(img_url)

    if img_response.status_code == 200:
        img_bytes = img_response.content # hold image in ram
        img_file = io.BytesIO(img_bytes) # send as Discord file attachment
        view = draw_view(prompt, message, api_content=prompt) # format Draw button
        await message.reply(file=discord.File(img_file, "output.png"), view=view) # reply with image, and view for button
        img_file.close() # close the new BytesIO object
    else:
        await message.reply("Failed to fetch the image.")

"""
run bot
"""
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler)
