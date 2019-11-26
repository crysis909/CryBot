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
        url = os.getenv("API_IMGFLIP").format(sub="get_memes")

        response = await api_get(url)

        memes = response["data"]["memes"]

        meme = random.choice(memes)
        meme_id = meme["id"]
        meme_name = meme["name"]
        meme_link = meme["url"]

        await ctx.send("ID: " + meme_id + "\n" + meme_name + "\n" + meme_link)

    @commands.command(name="genMeme", help="Creates a meme with top and bottom text on a specific image")
    async def genMeme(self, ctx, template_id : int, top : str, bottom : str):
        url = os.getenv("API_IMGFLIP").format(sub="caption_image")
        username = os.getenv("API_IMGFLIP_USERNAME")
        password = os.getenv("API_IMGFLIP_PASSWORD")

        data ={
            "template_id" : template_id,
            "username" : username,
            "password" : password,
            "text0" : top,
            "text1" : bottom
        }

        response = await api_post(url, data)
        success = response["success"]

        if success == False:
            output = response["error_message"]
        else:
            output = response["data"]["url"]

        await ctx.send(output)

    #TODO Multi-Language
    @commands.command(name="weather", help="Gets the current weather of the city")
    async def weather(self, ctx, city : str, units : str = "metric", lang : str = "de"):
        if not units in ("kelvin", "metric", "imperial"):
            raise ValueError("Only imperial, metric and kelvin are allowed")

        if units == "kelvin":
            temp_unit = " K"
            speed_unit = " meter/sec"
        elif units == "metric":
            temp_unit = " °C"
            speed_unit = " meter/sec"
        else:
            temp_unit = " °F"
            speed_unit = " miles/hour"

        url = os.getenv("API_WEATHER")
        author = os.getenv("API_WEATHER_AUTHOR")
        author_url = os.getenv("API_WEATHER_AUTHOR_URL")
        author_icon_url = os.getenv("API_WEATHER_AUTHOR_ICON")
        icon_url = os.getenv("API_WEATHER_ICON")
        city_url = os.getenv("API_WEATHER_CITY")

        params = {
            "q" : city,
            "lang" : lang,
            "units" : units
        }

        response = await api_get(url, params)

        weather = response["weather"][0]
        weather_description = weather["description"]
        weather_icon = weather["icon"]
        weather_icon_url = icon_url.format(icon_id=weather_icon)

        main = response["main"]
        main_temp = str(main["temp"]) + temp_unit
        main_temp_min = str(main["temp_min"]) + temp_unit
        main_temp_max = str(main["temp_max"]) + temp_unit
        main_pressure = str(main["pressure"]) + " hpa"
        main_humidity = str(main["humidity"]) + " %"

        visibility = str(response["visibility"]) + " m"

        wind = response["wind"]
        wind_speed = str(wind["speed"]) + speed_unit
        wind_deg = str(wind["deg"]) + " °"

        clouds = response["clouds"]["all"]

        sunrise_unix = response["sys"]["sunrise"]
        sunset_unix = response["sys"]["sunset"]

        sunrise = await unix2Date(sunrise_unix)
        sunset = await unix2Date(sunset_unix)

        city_id = response["id"]
        city_page = city_url.format(city_id=city_id)

        embed = discord.Embed(title=city.upper(), url=city_page)
        embed.set_author(name=author, url=author_url, icon_url=author_icon_url)
        embed.set_thumbnail(url=weather_icon_url)
        embed.add_field(name="Wetter", value=weather_description, inline=False)
        embed.add_field(name="Temperatur", value=main_temp, inline=True)
        embed.add_field(name="Max", value=main_temp_max, inline=True)
        embed.add_field(name="Min", value=main_temp_min, inline=True)
        embed.add_field(name="Sichtweite", value=visibility, inline=False)
        embed.add_field(name="Wind", value="\u200b", inline=False)
        embed.add_field(name="Geschwindigkeit", value=wind_speed, inline=True)
        embed.add_field(name="Grad", value=wind_deg, inline=True)
        embed.add_field(name="Wolken", value=clouds, inline=False)
        embed.add_field(name="Grad", value=wind_deg, inline=True)
        embed.add_field(name="Sonnenuntergang", value=sunset, inline=True)
        embed.add_field(name="Sonnenaufgang", value=sunrise, inline=True)

        embed.set_footer(
            text="Information provided by " + os.getenv("API_WEATHER_AUTHOR"), icon_url=os.getenv("API_WEATHER_AUTHOR_ICON")
        )

        await ctx.send(embed=embed)

    @commands.command(name="wiki", help="Gets an Wiki artikel back")
    async def wiki(self, ctx, term : str):
        url = os.getenv("API_WIKI")
        author = os.getenv("API_WIKI_AUTHOR")

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
            url = url.format(title.replace(" ", "_"))

        if len(description) > 1500:
            description = description[:1500].strip()
            description += "... [(read more)]({})".format(url)

            embed = discord.Embed(
                title="{}: {}".format(author, title),
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