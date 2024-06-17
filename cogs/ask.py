import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from helpers.pagination import send_paginated_message
from helpers.ai import get_response

class Ask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger
        self.conversation_histories = bot.conversation_histories
        self.last_interaction_times = {}
        self.clear_history.start()

    @commands.command(name="ask")
    async def ask(self, ctx) -> None:
        prompt = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()
        username = ctx.author.name
        user_id = ctx.author.id

        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []

        self.conversation_histories[user_id].append({"role": "user", "content": prompt})
        self.last_interaction_times[user_id] = datetime.now()
        
        async with ctx.channel.typing():
            try:
                response = get_response(self.conversation_histories[user_id])
                self.chat_logger.info(f"{username}: {prompt}\nVexel: {response}\n")
                if response:
                    self.conversation_histories[user_id].append({"role": "assistant", "content": response})
                    if len(response) >= 2000:
                        await send_paginated_message(ctx.channel, response)
                    else:
                        await ctx.reply(response)
                else:
                    await ctx.reply("Sorry, I couldn't answer you right now.")
            except Exception as e:
                self.chat_logger.error(f"Error processing ask command: {e}")
                await ctx.reply("An error occurred while processing your request.")
    
    @commands.command(name="reset")
    async def reset(self, ctx) -> None:
        user_id = ctx.author.id
        self.conversation_histories[user_id] = []
        self.last_interaction_times[user_id] = datetime.now()
        await ctx.reply("Your chat history has been reset.")
    
    @tasks.loop(hours=1)
    async def clear_history(self):
        now = datetime.now()
        to_remove = [user_id for user_id, last_interaction in self.last_interaction_times.items() if now - last_interaction > timedelta(hours=5)]
        for user_id in to_remove:
            del self.conversation_histories[user_id]
            del self.last_interaction_times[user_id]
            self.chat_logger.info(f"Cleared conversation history for user_id {user_id} due to inactivity.")
    
    @clear_history.before_loop
    async def before_clear_history(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            await self.on_mention(message)

    async def on_mention(self, message):
        username = message.author.name
        user_id = message.author.id
        mention_content = message.content.replace(f"<@!{self.bot.user.id}>", "").strip()

        if not mention_content:
            mention_content = "Hello, how can I assist you today?"

        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []

        self.conversation_histories[user_id].append({"role": "user", "content": mention_content})
        self.last_interaction_times[user_id] = datetime.now()
        
        async with message.channel.typing():
            try:
                response = get_response(self.conversation_histories[user_id])
                self.chat_logger.info(f"{username} mentioned: {mention_content}\nVexel: {response}\n")
                if response:
                    self.conversation_histories[user_id].append({"role": "assistant", "content": response})
                    if len(response) >= 2000:
                        await send_paginated_message(message.channel, response)
                    else:
                        await message.reply(response)
                else:
                    await message.reply("Sorry, I couldn't answer you right now.")
            except Exception as e:
                self.chat_logger.error(f"Error processing mention: {e}")
                await message.reply("An error occurred while processing your request.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ask(bot))

 