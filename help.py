async def help_command(message):
    HELP_TEXT = """
    > Hey there! I'm Vexel, an AI assistant discord bot!

   *Commands:*
  - `!ask ` `prompt ` - Ask a question for any information.
  - `!draw ` ` prompt ` - Request to generate an image based on your prompt.
    """ 
    
    await message.channel.send(HELP_TEXT) 
