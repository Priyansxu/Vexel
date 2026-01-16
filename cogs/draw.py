import io
import discord
from discord.ext import commands
from discord import app_commands, ui
from helpers.ai import edit_image
from PIL import Image

class Button(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.edit_original_response(view=self.view)
        await self.view.edit_image(interaction)

class View(ui.View):
    def __init__(self, prompt, image_bytes, message, api_content):
        super().__init__(timeout=180)
        self.prompt = prompt
        self.image_bytes = image_bytes
        self.message = message
        self.api_content = api_content
        self.add_item(Button())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(Button(label=label, disabled=disabled))

    async def edit_image(self, interaction: discord.Interaction = None):
        try:
            remix_image = edit_image(self.image_bytes, self.api_content)
            if remix_image and isinstance(remix_image, bytes):
                img_file = io.BytesIO(remix_image)
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

        if not await self.check_image_dimensions(interaction, image_bytes):
            return

        await interaction.response.defer(thinking=True)

        try:
            remix_image = edit_image(image_bytes, prompt)
            if remix_image and isinstance(remix_image, bytes):
                img_file = io.BytesIO(remix_image)
                file = discord.File(img_file, filename="image.png")

                await interaction.followup.send(file=file)

                message_obj = await interaction.original_response()
                await interaction.edit_original_response(view=View(prompt, image_bytes, message_obj, prompt))
            else:
                await interaction.followup.send("Failed to generate image.", ephemeral=True)
        except Exception:
            await interaction.followup.send("An error occurred.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Remix(bot))