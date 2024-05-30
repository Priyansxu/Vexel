import discord
from discord.ext import commands
from helpers.ai import recognize_image

class Look(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger

    @commands.command(name="look")
    async def look(self, ctx) -> None:
        username = ctx.author.name
        prompt = ctx.message.content
        if not prompt:
            prompt = "Describe the image"
        if ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            async with ctx.message.channel.typing():
                description = await recognize_image(attachment_url, prompt)
                self.chat_logger.info(f"{username}: {prompt}\nVexel: {description}\n")
                await ctx.reply(description)
        else:
            await ctx.reply("Please attach an image to analyze.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Look(bot))