import discord
from discord.ext import commands

class Greet(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="greet")
    @commands.is_owner()
    async def greet_command(self, ctx: commands.Context) -> None:
        greeting_message = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if "general" in channel.name or "chat" in channel.name:
                    try:
                        await channel.send(greeting_message)
                    except discord.Forbidden:
                        print(f"Permission denied to send message in {channel.name} of guild {guild.name}")
                    break

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Greet(bot))