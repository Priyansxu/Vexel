import discord
from discord.ext import commands
from text_by_api import get_openai_response

# Initialize the Discord bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ask'):
        prompt = message.content[5:].strip()
        response = get_openai_response(prompt)
        await message.channel.send(response)

# Run the bot with your Discord bot token
bot.run("YOUR_DISCORD_BOT_TOKEN")

