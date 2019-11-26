from datetime import datetime as dt
import aiohttp
import asyncio

async def unix2Date(unix : int):
    return dt.utcfromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S")

async def swap(x , y):
    x,y = y,x

    return x,y

async def now():
    return dt.now().strftime("%Y-%m-%d %H:%M:%S")

async def api_get(url, params : dict = None):
    """Return the JSON body of a call to Discord REST API."""
    headers = {"content-type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            print(await now(), "GET", response.url, "-->", response.status, response.reason)
            
            return await response.json()

async def api_post(url : str, data : dict):
    headers = {"accept": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            print(await now(), "POST", response.url, "-->", response.status, response.reason)
            return await response.json()

async def determine_prefix(bot, message):
    guild = message.guild
    #Only allow custom prefixs in guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes
