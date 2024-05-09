HELP_TEXT = """
**Commands:**
- ` !ask ` *prompt*
- ` !draw ` *prompt*
"""

async def help_command(ctx):
    await ctx.send(HELP_TEXT)
