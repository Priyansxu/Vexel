import discord
from discord.ext import commands
from helpers.ai import recognize_image

class Look(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.chat_logger = bot.chat_logger

    @commands.command(name="look")
    async def look(self, ctx: commands.Context) -> None:
        username = ctx.author.name
        prompt = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        if not prompt:
            prompt = "Describe the image"
        
        if ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            async with ctx.message.channel.typing():
                try:
                    description = await recognize_image(attachment_url, prompt)
                    self.chat_logger.info(f"{username}: {prompt}\nVexel: {description}\n")
                    await ctx.reply(description)
                except Exception as e:
                    self.chat_logger.error(f"Error recognizing image: {e}")
                    await ctx.reply("There was an error processing the image. Please try again.")
        else:
            await ctx.reply("Please attach an image to analyze.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Look(bot)) 