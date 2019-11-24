from discord.ext import commands

from classes.helper_funtions import swap
from classes.cog import Cog

import random


class Games(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="guess", help="Guess the right number between start and end")
    async def guess(self, ctx, guess:int, start:int=1, end:int=10):
        if end < start:
            await swap(start,end)

        choice = random.randint(start, end)
        chance = (start / (start + end) ) * 100

        if guess == choice:
            status = "WON"
        else:
            status = "LOST"

        output = "You ***{}*** the game\n".format(status)
        output += "The number ***{}*** was drawn, you guessed ***{}***. You had a chance of ***{}***% to guess right.".format(choice, guess, round(chance, 2))

        await ctx.send(output)

def setup(bot):
    bot.add_cog(Games(bot))