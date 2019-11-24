import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'loaded cog: {__name__}')

    async def cog_command_error(self, ctx, error):
        print(error)
        await ctx.send(error)