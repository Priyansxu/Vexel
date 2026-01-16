import discord
from discord.ext import commands
from discord import app_commands
from helpers.ai import get_response
from helpers.pagination import paginated_message
from helpers.prompt import SYSTEM_PROMPT

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "conversation_histories"):
            bot.conversation_histories = {}

    def _init_history(self, user_id: int):
        if user_id not in self.bot.conversation_histories:
            self.bot.conversation_histories[user_id] = [
                {
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT}]
                }
            ]

    @app_commands.command(name="chat", description="Chat with AI")
    @app_commands.describe(message="What is on your mind?")
    async def chat(self, interaction: discord.Interaction, message: str):
        user_id = interaction.user.id
        self._init_history(user_id)

        history = self.bot.conversation_histories[user_id]

        history.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        await interaction.response.defer()

        response = get_response(history)

        history.append({
            "role": "model",
            "parts": [{"text": response}]
        })

        if len(response) >= 2000:
            await paginated_message(interaction.channel, response)
        else:
            await interaction.followup.send(response)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            await self._handle_mention(message)

    async def _handle_mention(self, message: discord.Message):
        user_id = message.author.id
        self._init_history(user_id)

        content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not content:
            content = "Hello"

        history = self.bot.conversation_histories[user_id]

        history.append({
            "role": "user",
            "parts": [{"text": content}]
        })

        async with message.channel.typing():
            response = get_response(history)

        history.append({
            "role": "model",
            "parts": [{"text": response}]
        })

        if len(response) >= 2000:
            await paginated_message(message.channel, response)
        else:
            await message.reply(response)

async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))