import io
import discord
from discord.ext import commands
from discord import ui, app_commands
from helpers.ai import get_image

class Button(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.message.edit(view=self.view)
        await self.view.draw_image()

class View(ui.View):
    def __init__(self, prompt, message):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.add_item(Button())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(Button(label=label, disabled=disabled))

    async def draw_image(self):
        try:
            response = get_image(self.prompt)
            if response and isinstance(response, bytes):
                img_file = io.BytesIO(response)
                await self.message.edit(attachments=[discord.File(img_file, "image.png")])
                img_file.close()
            else:
                await self.message.edit(content="Failed to regenerate the image.")
        except Exception:
            pass
        finally:
            self.button_state('Regenerate', False)
            await self.message.edit(view=self)

class Draw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="draw", description="Generate an image")
    @app_commands.describe(prompt="The prompt for the image")
    async def draw(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        message = await interaction.followup.send("Drawing...")

        try:
            response = get_image(prompt)
            if response and isinstance(response, bytes):
                img_file = io.BytesIO(response)
                await message.edit(content=None, attachments=[discord.File(img_file, "image.png")])
                view = View(prompt, message)
                await message.edit(view=view)
                img_file.close()
            else:
                await message.edit(content="Failed to generate the image.")
        except Exception:
            await message.edit(content="An error occurred while processing your request.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Draw(bot))