import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Vexel - Help",
            description="Here are my commands:",
            color=discord.Color(0x871ef4),
            timestamp=ctx.message.created_at
        )

        embed.add_field(
            name="!ask [prompt]",
            value="Ask a question, I'll try to answer!",
            inline=False
        )

        embed.add_field(
            name="!draw [prompt]",
            value="Generate an image, text-to-image generation.",
            inline=False
        )

        embed.add_field(
            name="!look [attachment]",
            value="Recognize an image, get image description.",
            inline=False
        )

        embed.set_footer(text="Vexel AI")

        embed.set_image(url="https://cdn.discordapp.com/attachments/1246837283030565004/1250140939910123681/Untitled5.png?ex=6669dbfa&is=66688a7a&hm=638dd5c4df7bc54eccbc3e4282caa96af17f7b74148c316aab95079cf94623a5&")

        view = discord.ui.View()

        invite_button = discord.ui.Button(
            label="Invite",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1238461418999648277"
        )
        view.add_item(invite_button)

        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))