import discord
from discord import ui
from discord.ext import commands
from text_by_api import get_response
from edit_by_api import *
import os
import logging
import io
import torch
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.wuerstchen import DEFAULT_STAGE_C_TIMESTEPS

"""
debug logging
"""
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

"""
initialize text-to-image pipeline
"""
pipe = AutoPipelineForText2Image.from_pretrained("warp-ai/wuerstchen", torch_dtype=torch.float16).to("cuda")

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
intents.typing = False # can adjust these based on bot's needs
intents.presences = False
intents.message_content = True # enable message content intent

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

    
    if message.content.startswith('!draw'): # image controller using Diffusers
        await draw_image(prompt, message)

    if message.content.startswith('!edit'): # edit controller using API
        await edit_image(prompt, message)

"""      
split response message if over Discord's 2000 character limit
"""
async def send_paginated_message(channel, api_content, prompt, message):
    max_chars = 2000
    start = 0 # index 0 of text
    text = api_content

    while start < len(text): # iterate through text in chunks of 2000 characters
        end = start + max_chars # end index of each chunk
        if end > len(text):
            end = len(text) # prevent out of bounds error
        
        chunk = text[start:end] # escape / and > characters before sending
        chunk = chunk.replace('/', '\/')  # replace / with \/
        chunk = chunk.replace('>', '\>')  # replace > with \>


        if end >= len(text):
            view = draw_view(prompt, message, api_content) # creates Draw button
            await channel.send(chunk, view=view)
        else:
            await message.reply(chunk)

        start = end

        """
        if text[end:end + 1] == '\0':  # check for null character
            await channel.send(chunk)
            return
        else:
            await channel.send(chunk)
            start = end # update start index for next chunk
        """

"""
draw image
"""
async def draw_image(prompt, message):
    await message.reply("Drawing...") # command acknowledge message
    images = pipe(
        prompt, 
        width=2048,
        height=2048,
        prior_timesteps=DEFAULT_STAGE_C_TIMESTEPS,
        prior_guidance_scale=4.0,
        num_images_per_prompt=1
    ).images

    img_byte_arr = io.BytesIO() # hold image in ram
    images[0].save(img_byte_arr, format='PNG') # save file, convert from byte array to PNG
    img_byte_arr = img_byte_arr.getvalue()
    img_file = io.BytesIO(img_byte_arr) # send as Discord file attachment
    view = draw_view(prompt, message, api_content=prompt) # format Draw button
    await message.reply(file=discord.File(img_file, "output.png"), view=view) # reply with image, and view for button
    img_file.close() # close the new BytesIO object

"""
edit image
"""
async def edit_image(prompt, message):
    await message.reply("Editing...") # command acknowledge message
    filename = "image.png"

    if len(message.attachments) > 0:
        attachment = message.attachments[0] # retrieve attachment from message
        url = attachment.url # retrieve url from attachment
        # await message.reply(f"{url}") # replies with original image
        response = await download_image(url)
        if response is not None:
            with open(filename, 'wb') as f:
                f.write(response)
            check_and_resize_image(filename)
            # await message.reply(content="Resized", file=discord.File("img_resized.png", "output.png"))
            convert_image_to_rgba("img_resized.png")
            # await message.reply(content="Converted to RGBA", file=discord.File("img_rgba.png", "output.png"))
            make_image_transparent("img_rgba.png")
            await message.reply(content="Edit Area", file=discord.File("img_transparent.png", "output.png"))

    if prompt:
        img_url = get_edit("img_rgba.png", "img_transparent.png", prompt) # send edit request to api with prompt
    else:
        img_url = get_edit("img_rgba.png", "img_transparent.png") # send edit request to api without prompt

    # await message.reply(f"{img_url}") # testing function to ensure url is returned
    img_response = await download_image(img_url)

    if img_response is not None:
        img_file = io.BytesIO(img_response) # send as Discord file attachment
        # view = draw_view(prompt, message, api_content=prompt) # format Draw button
        await message.reply(content="Edit", file=discord.File(img_file, "output.png")) #, view=view) # reply with image, and view for button
        img_file.close() # close the new BytesIO object
    else:
        await message.reply("Failed to fetch the image.")



"""
run bot
"""
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler)
