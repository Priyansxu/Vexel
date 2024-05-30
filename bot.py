import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands
from ask import get_response
from draw import get_image
from help import help_command
from look import recognize_image
import os
import io
import requests
import logging
from dotenv import load_dotenv

"""
Load environment variables
"""
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

"""
debug logging
"""
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

"""
server logging
"""
server_handler = logging.FileHandler(filename='server.log', encoding='utf-8', mode='a')
server_logger = logging.getLogger('server')
server_logger.setLevel(logging.INFO)
server_logger.addHandler(server_handler)

"""
chat logging
"""
chat_handler = logging.FileHandler(filename='chats.log', encoding='utf-8', mode='a')
chat_logger = logging.getLogger('chat')
chat_logger.setLevel(logging.INFO)
chat_logger.addHandler(chat_handler)

"""
Bot intents and initialization
"""
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

"""
Button callback
"""
class DrawButton(ui.Button['DrawView']):
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await draw_image(self.view.api_content, self.view.message)

class DrawView(ui.View):
    def __init__(self, prompt, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.api_content = api_content
        self.add_item(DrawButton(label='Regenerate'))

def draw_view(prompt, message, api_content):
    return DrawView(prompt=prompt, message=message, api_content=api_content)

"""
Ready event
"""
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="@vexel & !help"))
    print(f'Logged in as {bot.user.name}')

"""
Guild join event
"""
@bot.event
async def on_guild_join(guild):
    server_name = guild.name
    server_owner = await guild.fetch_member(guild.owner_id)
    total_members = guild.member_count
    server_logger.info(f"Joined new server: {server_name}, Owner: {server_owner}, Total Members: {total_members}")

    channel_id = 1243869783406018640
    channel = bot.get_channel(channel_id)
    message = (
        f"Joined new server:\n"
        f"**Server Name:** {server_name}\n"
        f"**Owner:** {server_owner}\n"
        f"**Total Members:** {total_members}"
    )
    await channel.send(message)

"""
Main function to process messages
"""
conversation_histories = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    if user_id not in conversation_histories:
        conversation_histories[user_id] = []

    user_prompt = message.content
    username = message.author.name

    if bot.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if prompt:
            conversation_histories[user_id].append({"role": "user", "content": prompt})
            async with message.channel.typing():
                response = get_response(conversation_histories[user_id])
                chat_logger.info(f"{username}: {prompt}\nVexel: {response}\n")
                if response:
                    conversation_histories[user_id].append({"role": "assistant", "content": response})
                    if len(response) >= 2000:
                        await send_paginated_message(message.channel, response)
                    else:
                        await message.reply(response)
                else:
                    await message.reply("Sorry, I couldn't answer you right now.")
        else:
            await message.reply("Hey there, how can I assist you today? For commands, execute !help")
        return

    if message.content.startswith('!ask'):
        prompt = message.content[5:].strip()
        conversation_histories[user_id].append({"role": "user", "content": prompt})
        async with message.channel.typing():
            response = get_response(conversation_histories[user_id])
            chat_logger.info(f"{username}: {prompt}\nVexel: {response}\n")
            if response:
                conversation_histories[user_id].append({"role": "assistant", "content": response})
                if len(response) >= 2000:
                    await send_paginated_message(message.channel, response)
                else:
                    await message.reply(response)
            else:
                await message.reply("Sorry, I couldn't answer you right now.")

    elif message.content.startswith('!draw'):
        prompt = message.content[6:].strip()
        if not prompt:
            await message.channel.send("**Please provide image details.** \n\n> *example: !draw beautiful scenery of sunset.*")
        else:
            async with message.channel.typing():
                await draw_image(prompt, message)

    elif message.content.startswith('!look'):
        prompt = message.content[6:].strip()
        if not prompt:
            prompt = "Describe the image"
        if message.attachments:
            attachment_url = message.attachments[0].url
            async with message.channel.typing():
                description = await recognize_image(attachment_url, prompt)
                chat_logger.info(f"{username}: {prompt}\nVexel: {description}\n")
                await message.reply(description)
        else:
            await message.reply("Please attach an image to analyze.")

    elif message.content.startswith('!help'):
        async with message.channel.typing():
            await help_command(message)
            
    elif message.content.startswith('!reset'):
        conversation_histories[user_id] = []
        await message.reply("Your chat history has been reset.")
        
    elif message.content.startswith('!sayhi'):
        message = message.content[7:].strip()
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if "general" in channel.name or "chat" in channel.name:
                    try:
                        await channel.send(message)
                    except discord.Forbidden:
                        server_logger.info(f"Permission denied to send message in {channel.name} of guild {guild.name}")
                    break

"""
Function to split and send paginated message
"""
async def send_paginated_message(channel, api_content):
    max_chars = 2000
    start = 0
    text = api_content

    while start < len(text):
        end = start + max_chars
        if end > len(text):
            end = len(text)

        chunk = text[start:end]
        chunk = chunk.replace('/', '\/')
        chunk = chunk.replace('>', '\>')

        await channel.send(chunk)
        start = end

"""
Function to draw image
"""
async def draw_image(prompt, message):
    await message.reply("Drawing...")
    response = get_image(prompt)
    chat_logger.info(f"{message.author.name}: {prompt}\nVexel: {'Image generated' if response else 'Failed to generate image'}\n")

    if response is not None and isinstance(response, bytes):
        img_bytes = response
        img_file = io.BytesIO(img_bytes)
        view = draw_view(prompt, message, api_content=prompt)
        await message.reply(file=discord.File(img_file, "output.png"), view=view)
        img_file.close()
    else:
        await message.reply("Failed to generate the image.")

"""
Run bot
"""
bot.run(f"{DISCORD_BOT_TOKEN}", log_handler=handler) 