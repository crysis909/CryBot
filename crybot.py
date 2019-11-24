from dotenv import load_dotenv
from discord.ext import commands


from classes.helper_funtions import *

import discord
import youtube_dl
import asyncio
import classes.quote

import json
import random

import os

loop = None
custom_prefixes = {}
default_prefixes = ['!']

async def main():
    #############################################################################
    #                               START UP                                    #
    #############################################################################

    token = os.getenv("DISCORD_TOKEN")
    #yt_options = os.getenv("YT_OPTIONS")
    bot = commands.Bot(command_prefix=".")
    #bot = commands.Bot(command_prefix=".", owner_id=119837102199406593)
    
    #############################################################################
    #                            Bot Commands                                   #
    #############################################################################

    @commands.guild_only()
    @bot.command(name="setprefix", help="Changed the current prefix")
    async def setprefix(ctx, *, prefixes : str ="" ):
        global custom_prefixes, default_prefixes

        custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
        await ctx.send("Prefixes set!")

    @commands.is_owner()
    @bot.command(name="kill", aliases=["k", "die"], help="Kills the bot [Only Creator]")
    async def kill(ctx):
        try:
            await bot.close()
            await loop.close()
        except Exception as e:
            print(e)
            await ctx.send("{} You are not my creator, peasant!".format(ctx.author.mention))

    @commands.is_owner()
    @bot.command(name="add", aliases=["load"], help="Adds a cog")
    async def addCog(ctx, *, cog : str):
        try:
            bot.load_extension("cogs." + cog)
        except Exception as e:
            print(e)
            ctx.send(e.message)

    @commands.is_owner()
    @bot.command(name="remove", aliases=["unload"], help="Removes a cog")
    async def addCog(ctx, *, cog : str):
        bot.load_extension("cogs." + cog)

    @commands.is_owner()
    @bot.command(name="reload", help="Reloads a cog")
    async def reloadCog(ctx, *, cog : str):
            bot.reload_extension("cogs." + cog)

    #############################################################################
    #                               Bot Events                                  #
    #############################################################################

    @bot.event
    async def on_ready():
        print(f'Logged in as: {bot.user.name}')
        print(f'With ID: {bot.user.id}')

    @bot.event
    async def on_shard_ready(shard_id):
        print(shard_id)

    await bot.start(token)

if __name__ == "__main__":
    load_dotenv(verbose=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())