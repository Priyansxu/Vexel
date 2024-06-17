import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.server_logger = bot.server_logger

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        server_name = guild.name
        server_owner = guild.owner
        total_members = guild.member_count
        self.server_logger.info(f"Joined new server: {server_name}, Owner: {server_owner}, Total Members: {total_members}")

        channel_id = 1243869783406018640
        channel = self.bot.get_channel(channel_id)
        if channel:
            message = (
                f"Joined new server:\n"
                f"**Server Name:** {server_name}\n"
                f"**Owner:** {server_owner}\n"
                f"**Total Members:** {total_members}"
            )
            await channel.send(message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot)) 