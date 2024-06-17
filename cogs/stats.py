import discord
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='stats')
    async def stats(self, ctx: commands.Context):
        embed = discord.Embed(title="Bot Statistics", color=discord.Color(0x871ef4))

        total_guilds = len(self.bot.guilds)
        embed.add_field(name="Total Servers", value=total_guilds)

        ping_latency = self.bot.latency * 1000
        embed.add_field(name="Ping Latency", value=f"{ping_latency:.2f} ms")
        
        embed.add_field(name="Developer", value="`@priyansxu`")

        embed.add_field(name="Vexel Created", value="<t:1715293531:R>")

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot)) 