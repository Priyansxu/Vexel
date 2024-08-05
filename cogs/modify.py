import io
import discord
from discord.ext import commands
from discord import app_commands, ui
from helpers.ai import edit_image
from PIL import Image

class EditButton(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.message.edit(view=self.view)
        await self.view.edit_image()

class EditView(ui.View):
    def __init__(self, prompt, image_bytes, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.image_bytes = image_bytes
        self.message = message
        self.api_content = api_content
        self.add_item(EditButton())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(EditButton(label=label, disabled=disabled))

    async def edit_image(self):
        try:
            generated_images = edit_image(self.image_bytes, self.api_content)
            if generated_images and isinstance(generated_images[0], bytes):
                img_file = io.BytesIO(generated_images[0])
                await self.message.edit(attachments=[discord.File(img_file, "image.png")])
                img_file.close()
            else:
                await self.message.edit(content="Failed to regenerate the image.")
        except Exception as e:
            await self.message.edit(content=f"Failed to generate image: {e}")
        self.button_state('Regenerate', False)
        await self.message.edit(view=self)

class Modify(commands.Cog):
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
        except Exception as e:
            await interaction.response.send_message(f"Failed to check image dimensions: {e}", ephemeral=True)
            return False

    @app_commands.command(name="modify", description="Modify an image")
    @app_commands.describe(image="The image to modify", prompt="What changes you would like?")
    async def edit(self, interaction: discord.Interaction, image: discord.Attachment, prompt: str):
        image_bytes = await image.read()

        await interaction.response.defer()
        try:
            if not await self.check_image_dimensions(interaction, image_bytes):
                return

            generated_images = edit_image(image_bytes, prompt)

            if generated_images and isinstance(generated_images[0], bytes):
                img_file = io.BytesIO(generated_images[0])
                message = await interaction.followup.send(file=discord.File(img_file, "image.png"))
                view = EditView(prompt, image_bytes, message, prompt)
                await message.edit(view=view)
                img_file.close()
            else:
                await interaction.followup.send("Failed to generate the image.")
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Modify(bot)) 