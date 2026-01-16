import discord
from discord.ext import commands
from discord import app_commands
from helpers.pagination import paginated_message
from helpers.ai import get_response

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chat", description="Start chatting with AI")
    @app_commands.describe(message="What is in your mind?")
    async def chat(self, interaction: discord.Interaction, message: str):
        user_id = interaction.user.id
        chat_histories = self.bot.conversation_histories

        if user_id not in chat_histories:
            chat_histories[user_id] = []

        chat_histories[user_id].append({
    "role": "user",
    "parts": [{"type": "text", "text": message}]
})

        await interaction.response.defer()

        try:
            response = get_response(chat_histories[user_id])
            if response:
                chat_histories[user_id].append({
    "role": "model",
    "parts": [{"type": "text", "text": response}]
})
                if len(response) >= 2000:
                    await paginated_message(interaction.channel, response)
                else:
                    await interaction.followup.send(response)
            else:
                await interaction.followup.send("Sorry, I couldn't answer you right now.")
        except Exception as e:
            await interaction.followup.send("Ugh, my brain hurts, can you say that again?")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            await self.on_mention(message)

    async def on_mention(self, message):
        user_id = message.author.id
        mention_content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not mention_content:
            mention_content = "Hello, how can I assist you today?"

        chat_histories = self.bot.conversation_histories

        if user_id not in chat_histories:
            chat_histories[user_id] = []

        chat_histories[user_id].append({"role": "user", "parts": [mention_content]})

        async with message.channel.typing():
            try:
                response = get_response(chat_histories[user_id])
                if response:
                    chat_histories[user_id].append({"role": "model", "parts": [response]})
                    if len(response) >= 2000:
                        await paginated_message(message.channel, response)
                    else:
                        await message.reply(response)
                else:
                    await message.reply("Sorry, I couldn't answer you right now.")
            except Exception as e:
                print(f"Error in on_mention: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chat(bot))