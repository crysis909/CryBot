from discord.ext import commands
from classes.helper_funtions import *
import discord

from classes.cog import Cog

import os
import random

class Api(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="meme", help="Get's an specific or random meme from imgflip")
    async def meme(self, ctx):
        response = await api_get(os.getenv("API_IMGFLIP").format(sub="get_memes"))

        memes = response["data"]["memes"]

        meme = random.choice(memes)
        meme_id = meme["id"]
        meme_name = meme["name"]
        meme_link = meme["url"]

        await ctx.send("ID: " + meme_id + "\n" + meme_name + "\n" + meme_link)

    @commands.command(name="genMeme", help="Creates a meme with top and bottom text on a specific image")
    async def genMeme(self, ctx, template_id : int, top : str, bottom : str):
        api_url = os.getenv("API_IMGFLIP").format(sub="caption_image")
        username = os.getenv("API_IMGFLIP_USERNAME")
        password = os.getenv("API_IMGFLIP_PASSWORD")

        data ={
            "template_id" : template_id,
            "username" : username,
            "password" : password,
            "text0" : top,
            "text1" : bottom
        }

        response = await api_post(api_url, data)
        success = response["success"]

        if success == False:
            output = response["error_message"]
        else:
            output = response["data"]["url"]

        await ctx.send(output)

    @commands.command(name="wiki", help="Get's an Wiki artikel back")
    async def wiki(self, ctx, term):
        url = os.getenv("API_WIKI")

        params = {
            "action": "query",
            "titles": term,
            "format": "json",
            "formatversion": "2",
            "prop": "extracts",
            "exintro": "1",
            "redirects": "1",
            "explaintext": "1"
        }

        response = await api_get(url, params)

        for page in response["query"]["pages"]:
            title = page["title"]
            description = page["extract"].strip().replace("\n", "\n\n")
            url = os.getenv("API_WIKI").format(title.replace(" ", "_"))

        if len(description) > 1500:
            description = description[:1500].strip()
            description += "... [(read more)]({})".format(url)

            embed = discord.Embed(
                title="Wikipedia: {}".format(title),
                description=u"{}".format(description),
                color=discord.Color.blue(),
                url=url,
            )

            embed.set_footer(
                text="Information provided by Wikimedia", icon_url=os.getenv("API_WIKI_ICON")
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Api(bot))