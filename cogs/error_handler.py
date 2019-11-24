from discord.ext import commands

import discord

from classes.cog import Cog
from classes.logger import Logger

class CommandErrorHandler(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.logger = Logger("CryBot", "logs")

    async def cog_command_error(self, ctx, error):
        self.logger.error(error.message)
        ctx.send(error.message)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))