import discord
from discord.ext import commands
import urllib.parse

class Google(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='google', help='Search LMGTFY')
    async def google(self, ctx: commands.Context, *, query: str):
        google_url = "https://letmegooglethat.com"
        params = {"q": query}
        search_url = f"{google_url}?{urllib.parse.urlencode(params)}"
        
        embed = discord.Embed(
            title="LMGTFY Search",
            description=f"Click [here]({search_url}) to see the search results for: **{query}**",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Google(bot))