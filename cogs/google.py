import discord
from discord.ext import commands
import urllib.parse

class GoogleButton(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()
        self.add_item(discord.ui.Button(label=label, url=url))

class Google(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="google")
    async def google(self, ctx: commands.Context) -> None:
        query = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        if not query:
            await ctx.send("Please provide a search query.")
            return
        
        google_url = "https://letmegooglethat.com"
        params = {"q": query}
        search_url = f"{google_url}?{urllib.parse.urlencode(params)}"
        
        embed = discord.Embed(
            title="Google",
            description=f"Click the button below (;",
            color=discord.Color(0x871ef4)
        )

        view = GoogleButton(label=query, url=search_url)
        
        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Google(bot))