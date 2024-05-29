async def help_command(message):
    HELP_TEXT = """
    > Hey there! I'm **Vexel**, an AI assistant Discord bot! You can mention me in your message, and I'll respond to you.

### Commands:
- `!ask ` `prompt ` - *Ask a question, i'll try to answer!*

- `!draw ` ` prompt ` - *Generate an image, text-to-image generation.*

- `!look ` ` attachment ` - *Recognise an image, get image description.*
    """ 
    
    await message.channel.send(HELP_TEXT) 