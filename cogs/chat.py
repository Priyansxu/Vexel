import discord
from discord.ext import commands
from discord import app_commands
from helpers.pagination import send_paginated_message
from helpers.ai import get_response

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_histories = {}

    @app_commands.command(name="chat", description="Start chatting with Ai")
    @app_commands.describe(message="What is in your mind?")
    async def chat(self, interaction: discord.Interaction, message: str):
        user_id = interaction.user.id

        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []

        self.chat_histories[user_id].append({"role": "user", "parts": [message]}) 

        await interaction.response.defer()

        try:
            response = get_response(self.chat_histories[user_id])
            if response:
                self.chat_histories[user_id].append({"role": "model", "parts": [response]}) 
                if len(response) >= 2000:
                    await send_paginated_message(interaction.channel, response)
                else:
                    await interaction.followup.send(response)
            else:
                await interaction.followup.send("Sorry, I couldn't answer you right now.")
        except Exception as e:
            await interaction.followup.send(f"Ugh, my brain hurts, can you say that again?")

    @app_commands.command(name="wipe", description="Wipe chat history")
    async def wipe(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id in self.chat_histories:
            self.chat_histories[user_id] = []
            await interaction.response.send_message("Your chat history has been wiped.")
        else:
            await interaction.response.send_message("You don't have any chat history with me")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            await self.on_mention(message)

    async def on_mention(self, message):
        username = message.author.name
        user_id = message.author.id
        mention_content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not mention_content:
            mention_content = "Hello, how can I assist you today?"

        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []

        self.chat_histories[user_id].append({"role": "user", "parts": [mention_content]}) 

        async with message.channel.typing():
            try:
                response = get_response(self.chat_histories[user_id])
                if response:
                    self.chat_histories[user_id].append({"role": "model", "parts": [response]})
                    if len(response) >= 2000:
                        await send_paginated_message(message.channel, response)
                    else:
                        await message.reply(response)
                else:
                    await message.reply("Sorry, I couldn't answer you right now.")
            except Exception as e:
                print(f"Error in on_mention: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chat(bot)) 
