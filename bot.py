import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands
from ask import get_response
from draw import get_image
from help import help_command
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
        self.add_item(DrawButton(label='Regenerate'))

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
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print(f'Logged in as {bot.user.name}')

"""
main function to process message
"""
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    prompt = message.content[5:].strip() # get prompt from message content

    if message.content.startswith('!ask'):
        async with message.channel.typing():
            response = get_response(prompt)  # get response from API
            if response:
                api_content = response  # assuming response is already the content
                if len(api_content) >= 2000:  # paginate response if over Discord's character limit
                    await send_paginated_message(message.channel, api_content)
                else:
                    await message.reply(api_content)
  
    elif message.content.startswith('!draw'): # image controller using Stable Diffusion API
        if len(prompt) == 0:  # Check if user included image details
            await message.channel.send("**Please provide image details.** \n\n> *example: !draw beautiful scenery of sunset.*")
        else:
            async with message.channel.typing():
                await draw_image(prompt, message)
        
    elif message.content.startswith('!help'): # help command
        async with message.channel.typing():
            await help_command(message)

"""      
split response message if over Discord's 2000 character limit
"""
async def send_paginated_message(channel, api_content):
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

        await channel.send(chunk)
        start = end
 
"""
draw image using Stable Diffusion API
""" 
async def draw_image(prompt, message):
    await message.reply("Drawing...") # command acknowledge message
    response = get_image(prompt)
 
    if response is not None and isinstance(response, bytes):
        img_bytes = response
        img_file = io.BytesIO(img_bytes)  # Send as Discord file attachment
        view = draw_view(prompt, message, api_content=prompt)  # Format Draw button
        await message.reply(file=discord.File(img_file, "output.png"), view=view)  # Reply with image, and view for button
        img_file.close()  # Close the new BytesIO object
    else:
        await message.reply("Failed to generate the image.") 

"""
run bot
"""
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler) 