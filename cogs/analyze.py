import discord
from discord.ext import commands
from discord import app_commands
from helpers.ai import recognize_image

class Analyze(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="analyze", description="Analyze an image")
    @app_commands.describe(image="The image to analyze", prompt="The prompt for image description")
    async def analyze(self, interaction: discord.Interaction, image: discord.Attachment, prompt: str = "Describe the image") -> None:
        username = interaction.user.name
        await interaction.response.defer()
        
        try:
            image_data = await image.read()
            description = await recognize_image(image_data, prompt)
            await interaction.followup.send(description)
        except Exception as e:
            await interaction.followup.send("There was an error processing the image. Please try again.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Look(bot)) 
