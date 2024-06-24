import discord
from discord.ext import commands
from discord import app_commands
import urllib.parse

class GoogleButton(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()
        self.add_item(discord.ui.Button(label=label, url=url))

class Google(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="google", description="Search somthing on google")
    @app_commands.describe(search="The search query to look up on Google")
    async def google(self, interaction: discord.Interaction, search: str) -> None:
        google_url = "https://letmegooglethat.com"
        params = {"q": search}
        search_url = f"{google_url}?{urllib.parse.urlencode(params)}"

        view = GoogleButton(label=search, url=search_url)

        await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Google(bot)) 