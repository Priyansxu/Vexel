import discord
from discord.ext import commands
from discord import app_commands

class Wipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="wipe", description="Wipe chat history")
    async def wipe(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        chat_histories = self.bot.conversation_histories

        if user_id in chat_histories:
            chat_histories[user_id] = []
            await interaction.response.send_message("Your chat history has been wiped.")
        else:
            await interaction.response.send_message("You don't have any chat history with me")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Wipe(bot))