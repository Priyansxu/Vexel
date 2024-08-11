import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Display list of commands")
    async def help_command(self, interaction: discord.Interaction) -> None:
  
        embed = discord.Embed(
            title="Vexel - Commands",
            color=discord.Color(0x871ef4),
            timestamp=interaction.created_at 
        )

        embed.add_field(
            name="/chat",
            value="Start chating with Vexel.",
            inline=False
        )

        embed.add_field(
            name="/draw",
            value="Generate an image, text-to-image generation.",
            inline=False
        )

        embed.add_field(
            name="/analyze",
            value="Recognize an image, get image description.",
            inline=False
        ) 
        
        embed.add_field(
            name="/modify",
            value="Modify an image, make visual changes.",
            inline=False
        ) 
  
        embed.add_field(
            name="/wipe",
            value="Wipe your chat history with Vexel.",
            inline=False
        )
       embed.set_image(url="https://vexel.vercel.app/vexel_header.png")

        view = discord.ui.View()

        invite_button = discord.ui.Button(
            label="Add",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1238461418999648277"
        )
        view.add_item(invite_button)

        support_button = discord.ui.Button(
            label="Community",
            style=discord.ButtonStyle.link,
            url="https://discord.com/invite/b8EUTGC4Uw"
        )
        view.add_item(support_button)

        async def info_embed(interaction: discord.Interaction):
            embed = discord.Embed(
                title="Vexel - Information",
                color=discord.Color(0x871ef4)
            )

            total_guilds = len(self.bot.guilds)
            embed.add_field(name="Total Servers", value=total_guilds)

            ping_latency = self.bot.latency * 1000
            embed.add_field(name="Ping Latency", value=f"{ping_latency:.2f} ms")

            embed.add_field(name="Vexel Created", value="<t:1715293531:R>")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        info_button = discord.ui.Button(label="Info", style=discord.ButtonStyle.primary)
        info_button.callback = info_embed
        view.add_item(info_button)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot)) 