import io
import discord
from discord.ext import commands
from discord import ui
from helpers.ai import get_image

class DrawButton(ui.Button):
    def __init__(self, label='Regenerate', disabled=False):
        super().__init__(label=label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.button_state('Regenerating...', True)
        await interaction.message.edit(view=self.view)
        await self.view.draw_image()

class DrawView(ui.View):
    def __init__(self, prompt, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.api_content = api_content
        self.add_item(DrawButton())

    def button_state(self, label, disabled):
        self.clear_items()
        self.add_item(DrawButton(label=label, disabled=disabled))

    async def draw_image(self):
        response = get_image(self.api_content)
        if response and isinstance(response, bytes):
            img_file = io.BytesIO(response)
            await self.message.edit(attachments=[discord.File(img_file, "image.png")])
            img_file.close()
        else:
            await self.message.edit(content="Failed to regenerate the image.")
        self.button_state('Regenerate', False)
        await self.message.edit(view=self)

class Draw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger

    @commands.command(name="draw")
    async def draw(self, ctx):
        prompt = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        if not prompt:
            await ctx.send("**Please provide image details.**\n> *example: !draw beautiful scenery of sunset.*")
            return

        async with ctx.typing():
            await ctx.reply("Drawing...")
            response = get_image(prompt)
            self.chat_logger.info(f"{ctx.author.name}: {prompt}\nVexel: {'Image generated' if response else 'Failed to generate image'}\n")
            if response and isinstance(response, bytes):
                img_file = io.BytesIO(response)
                message = await ctx.reply(file=discord.File(img_file, "image.png"))
                view = DrawView(prompt, message, prompt)
                await message.edit(view=view)
                img_file.close()
            else:
                await ctx.reply("Failed to generate the image.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Draw(bot)) 