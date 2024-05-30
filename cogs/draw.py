import io
import discord
from discord.ext import commands
from discord import ui
from discord.ui import Button, View
from helpers.ai import get_image, draw_image

# Button callback
class DrawButton(ui.Button['DrawView']):
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await draw_image(self.view.api_content, self.view.message)

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


class Draw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger
    
    @commands.command(name="draw")
    async def draw(self, ctx) -> None:
        prompt = ctx.message.content
        if not prompt:
            await ctx.channel.send("**Please provide image details.** \n\n> *example: !draw beautiful scenery of sunset.*")
            return
        async with ctx.channel.typing():
            await ctx.reply("Drawing...")
            response = get_image(prompt)
            self.chat_logger.info(f"{ctx.author.name}: {prompt}\nVexel: {'Image generated' if response else 'Failed to generate image'}\n")
            if response is not None and isinstance(response, bytes):
                img_bytes = response
                img_file = io.BytesIO(img_bytes)
                view = DrawView.draw_view(prompt, ctx.message, api_content=prompt)
                await ctx.reply(file=discord.File(img_file, "output.png"), view=view)
                img_file.close()
            else:
                await ctx.reply("Failed to generate the image.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Draw(bot))
