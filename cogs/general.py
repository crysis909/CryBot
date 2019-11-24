# Member beleidigen (Voice)
from discord.ext import commands

from classes.helper_funtions import swap
from classes.cog import Cog


import discord
import random


class General(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        
    @commands.command(name="coin", help="Flips a coin x times")
    async def coin(self, ctx, times:int=1):
        max_flips = 10
        if times > max_flips:
            await self, ctx.send("Too many flips. MAX: " + str(max_flips))
            return

        coin_sides = ["Kopf", "Zahl"]
        choices = random.choices(coin_sides, k=times)
        
        for count, choice in enumerate(choices, 1):
            await self, ctx.send(str(count) + ": " + choice)

    @commands.command(name="random", help="Random number between start and end")
    async def random_(self, ctx, start:int, end:int):
        if end < start:
            start,end = await swap(start,end)
            
        await self, ctx.send(random.randint(start, end))

    @commands.command(name="choose", help="Choose between mulitple options")
    async def choose(self, ctx, *choices):
        if len(choices) < 2:
            await self, ctx.send("Not enough options available")
        else:
            await self, ctx.send(random.choice(choices))

    @commands.command(name="offend", help="Offends the given member")
    async def offend(self, ctx, member : discord.Member):
        offends = []
        pass

    @commands.command(name="quote", help="Sends a random quote of a specificite group")
    async def quote(self, ctx, group):
        quotes = {
            "darksouls" : [
                "Git gud ~OnlyAfro",
                "Solaire of Astora is a fictional knight from the 2011 action role-playing game Dark Souls. He has received a great deal of popularity amongst fans for his unusually friendly and helpful demeanor, as well as his signature gesture, 'Praise the Sun', which involves holding up both arms in a Y-shape while standing on tiptoes. He is voiced by Daniel Flynn. ~Solaire of Astora",
                "The beings who possess these souls have outlived their their usefulness, or chosen the path of the wicked. Let there be no guilt - let there be no vacillation. ~Kingseeker Frampt"
            ],

            "spongebob" : [

            ]
        }

def setup(bot):
    bot.add_cog(General(bot))