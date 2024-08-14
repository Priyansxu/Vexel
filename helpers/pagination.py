import discord

async def paginated_message(channel, api_content):
    max_chars = 2000
    start = 0
    text = api_content
    while start < len(text):
        end = start + max_chars
        if end > len(text):
            end = len(text)
        chunk = text[start:end]
        chunk = chunk.replace('/', r'\/')
        chunk = chunk.replace('>', r'\>')
        await channel.send(chunk)
        start = end