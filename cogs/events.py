import discord
from discord.ext import commands
from helpers.pagination import send_paginated_message
from helpers.ai import get_response

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.chat_logger = bot.chat_logger
        self.server_logger = bot.server_logger
        self.conversation_histories = bot.conversation_histories
    
    # Guild join event
    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> None:
        server_name = guild.name
        server_owner = await guild.fetch_member(guild.owner_id)
        total_members = guild.member_count
        self.server_logger.info(f"Joined new server: {server_name}, Owner: {server_owner}, Total Members: {total_members}")
    
        channel_id = 1243869783406018640  # Adjust this channel ID as needed
        channel = self.bot.get_channel(channel_id)
        message = (
            f"Joined new server:\n"
            f"**Server Name:** {server_name}\n"
            f"**Owner:** {server_owner}\n"
            f"**Total Members:** {total_members}"
        )
        await channel.send(message)
     
    # Message listener
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author.bot:
            return
        
        user_id = str(message.author.id)
        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []
    
        user_prompt = message.content
        username = message.author.name
    
        if self.bot.user.mentioned_in(message):
            prompt = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            if prompt:
                self.conversation_histories[user_id].append({"role": "user", "content": prompt})
                async with message.channel.typing():
                    response = get_response(self.conversation_histories[user_id])
                    self.chat_logger.info(f"{username}: {prompt}\nVexel: {response}\n")
                    if response:
                        self.conversation_histories[user_id].append({"role": "assistant", "content": response})
                        if len(response) >= 2000:
                            await send_paginated_message(message.channel, response)
                        else:
                            await message.reply(response)
                    else:
                        await message.reply("Sorry, I couldn't answer you right now. You can use !draw cmnd for now! Thanku")
            else:
                await message.reply("Hey there, how can I assist you today? For commands, execute !help")
            return
          

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
