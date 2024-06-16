import io
import discord
from discord.ext import commands
from discord import ui
from discord.ui import Button, View
from helpers.ai import get_image

class DrawButton(ui.Button['DrawView']):
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        self.view.clear_items()
        self.view.add_item(RegeneratingButton(label='Regenerating...', disabled=True))
        await interaction.message.edit(view=self.view)
        await self.view.draw_image(self.view.api_content, self.view.message)

class RegeneratingButton(ui.Button['DrawView']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DrawView(ui.View):
    def __init__(self, prompt, message, api_content):
        super().__init__()
        self.prompt = prompt
        self.message = message
        self.api_content = api_content
        self.add_item(DrawButton(label='Regenerate'))

    @staticmethod
    def draw_view(prompt, message, api_content):
        return DrawView(prompt=prompt, message=message, api_content=api_content)

    async def draw_image(self, api_content, message):
        response = get_image(api_content)
        if response is not None and isinstance(response, bytes):
            img_bytes = response
            img_file = io.BytesIO(img_bytes)
            await message.edit(attachments=[discord.File(img_file, "vexel.png")])
            img_file.close()
        else:
            await message.edit(content="Failed to regenerate the image.")
        
        self.clear_items()
        self.add_item(DrawButton(label='Regenerate'))
        await message.edit(view=self)

class Draw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger
    
    @commands.command(name="draw")
    async def draw(self, ctx) -> None:
        prompt = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        if not prompt:
            await ctx.channel.send("**Please provide image details.**\n\n> *example: !draw beautiful scenery of sunset.*")
            return
        
        async with ctx.channel.typing():
            await ctx.reply("Drawing...")
            response = get_image(prompt)
            self.chat_logger.info(f"{ctx.author.name}: {prompt}\nVexel: {'Image generated' if response else 'Failed to generate image'}\n")
            if response is not None and isinstance(response, bytes):
                img_bytes = response
                img_file = io.BytesIO(img_bytes)
                message = await ctx.reply(file=discord.File(img_file, "vexel.png"))
                view = DrawView.draw_view(prompt, message, api_content=prompt)
                await message.edit(view=view)
                img_file.close()
            else:
                await ctx.reply("Failed to generate the image.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Draw(bot))