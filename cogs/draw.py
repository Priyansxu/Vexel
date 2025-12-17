import io
import discord
from discord.ext import commands
from discord import ui, app_commands
from helpers.ai import get_image

class Button(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.edit_original_response(view=self.view)
        await self.view.draw_image(interaction)

class View(ui.View):
    def __init__(self, prompt, message):
        super().__init__(timeout=180)
        self.prompt = prompt
        self.message = message
        self.add_item(Button())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(Button(label=label, disabled=disabled))

    async def draw_image(self, interaction: discord.Interaction = None):
        try:
            response = get_image(self.prompt)
            if response and isinstance(response, bytes):
                img_file = io.BytesIO(response)
                file = discord.File(img_file, filename="image.png")
                
                if interaction:
                    await interaction.edit_original_response(attachments=[file])
                else:
                    await self.message.edit(attachments=[file])
            else:
                if interaction:
                    await interaction.followup.send("Failed to regenerate.", ephemeral=True)
                else:
                    await self.message.edit(content="Failed to regenerate the image.")
        except Exception:
            pass
        finally:
            self.button_state('Regenerate', False)
            if interaction:
                await interaction.edit_original_response(view=self)
            else:
                await self.message.edit(view=self)

class Draw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="draw", description="Generate an image")
    @app_commands.describe(prompt="The prompt for the image")
    async def draw(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)

        try:
            response = get_image(prompt)
            if response and isinstance(response, bytes):
                img_file = io.BytesIO(response)
                file = discord.File(img_file, filename="image.png")
                
                await interaction.followup.send(file=file)
                
                message_obj = await interaction.original_response()
                await interaction.edit_original_response(view=View(prompt, message_obj))
            else:
                await interaction.followup.send("Failed to generate image.", ephemeral=True)
        except Exception:
            await interaction.followup.send("An error occurred.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Draw(bot))
