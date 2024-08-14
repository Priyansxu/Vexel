import io
import discord
from discord.ext import commands
from discord import app_commands, ui
from helpers.ai import edit_image
from PIL import Image

class Button(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.message.edit(view=self.view)
        await self.view.edit_image()

class View(ui.View):
    def __init__(self, prompt, image_bytes, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.image_bytes = image_bytes
        self.message = message
        self.api_content = api_content
        self.add_item(Button())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(Button(label=label, disabled=disabled))

    async def edit_image(self):
        try:
            remix_image = edit_image(self.image_bytes, self.api_content)
            if remix_image and isinstance(remix_image, bytes):
                img_file = io.BytesIO(remix_image)
                await self.message.edit(attachments=[discord.File(img_file, "image.png")])
                img_file.close()
            else:
                await self.message.edit(content="Failed to regenerate the image.")
        except Exception:
            pass
        finally:
            self.button_state('Regenerate', False)
            await self.message.edit(view=self)

class Remix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def check_image_dimensions(self, interaction, image_bytes):
        try:
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size

            if width < 320 or width > 1536 or height < 320 or height > 1536:
                await interaction.response.send_message("Image dimensions must be between 320 and 1536 pixels.", ephemeral=True)
                return False

            return True
        except Exception:
            return False

    @app_commands.command(name="remix", description="Remix an image")
    @app_commands.describe(image="The image to remix", prompt="What changes you would like in the image?")
    async def remix(self, interaction: discord.Interaction, image: discord.Attachment, prompt: str):
        image_bytes = await image.read()

        await interaction.response.defer()
        message = await interaction.followup.send("Remixing...")

        try:
            if not await self.check_image_dimensions(interaction, image_bytes):
                return

            remix_image = edit_image(image_bytes, prompt)

            if remix_image and isinstance(remix_image, bytes):
                img_file = io.BytesIO(remix_image)
                await message.edit(content=None, attachments=[discord.File(img_file, "image.png")])
                view = View(prompt, image_bytes, message, prompt)
                await message.edit(view=view)
                img_file.close()
            else:
                await message.edit(content="Failed to generate the image.")
        except Exception:
            await message.edit(content="An error occurred while processing your request.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Remix(bot))