import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @commands.command(name="help")
    async def help_command(self, ctx) -> None:
        HELP_TEXT = """
        > Hey there! I'm **Vexel**, an AI assistant Discord bot! You can mention me in your message, and I'll respond to you.
    
    ### Commands:
    - `!ask ` `prompt ` - *Ask a question, i'll try to answer!*
    
    - `!draw ` ` prompt ` - *Generate an image, text-to-image generation.*
    
    - `!look ` ` attachment ` - *Recognise an image, get image description.*
        """ 
        
        await ctx.channel.send(HELP_TEXT) 

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))