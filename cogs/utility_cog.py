"""
File: utility_cog.py
defines simple utility commands in a cog class!
Contributors: Bryan Robbins, Karl Miller
Created: 3/21/2021
Updated: 3/21/2021
"""
from discord.ext import commands
import requests
import json
import random
from our_packages.api_manager import getrequest


class UtilityCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def randrange(self, ctx, start, end):
        """
        gets a rnadom number in range
        :return: result of coin flip
        """

        flip = random.randint(int(start), int(end))
        await ctx.send(flip)

    @commands.command(pass_context=True)
    async def idea(self,ctx, seed=-1):
        """
        generates random game idea using karl's game idea generation functions
        :param seed:
        :return: random game idea
        """
        response = requests.get("http://127.0.0.1:5000/randidea?key=DgGl3ju8ftRF494B7kQAInDl80bWqUbeG6hQBRgCI52MknkLhv61dVlpZflfjhHDC2Y9Nk3wcd7tDQVUK9usW34CZ1r7wCxf18PZ&seed=-1")
        idea = response.content.decode("utf-8")
        await ctx.send(f"```{idea}```")

    @commands.command(pass_context=True, aliases=["weather","weatherat"])
    async def weather_at(self, ctx, lat=None, lon=None):
        """
        Returns weather at specific latitude and longitude
        :param ctx: message context
        :param lat: latitude of location OR zipcode, in case of zipcode lon must not be passed
        :param lon: longitude of location
        :return: weather at lat,lon
        """
        if not lon:  # in the case of only zip code provided
            response = requests.get(f"https://www.zipcodeapi.com/rest/3zsGNFbsiyugtCBBSMg3egFK5vfJXb4LCYiY7EGskMb9LhUS8xEzlvmDJJi6Ikc9/info.json/{lat}/degrees")
            res = json.loads(response.content)
            if "error_code" in res.keys():
                await ctx.send("Invalid zip code!")
                return 500
            print(res)
            lat = res['lat']
            lon = res['lng']
            city = res['city']
            state = res['state']

            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
                                    + "&appid=7d7da9cec04671cc03ef4220ca73d0bf")
            res = json.loads(response.content)

            weather = res['weather'][0]['description']
            temp = format((res['main']['temp'] - 273.15) * 1.8 + 32, '.2f')
            feels_like = format((res['main']['feels_like'] - 273.15) * 1.8 + 32, '.2f')
            humidity = format(res['main']['humidity'], '.2f')

            await ctx.send(
                f"```Here Is the weather info for {city}, {state}:\n    Weather: {weather}\n    Temp: {temp}f\n    Feels like: {feels_like}f\n    Humidity: {humidity}```")

        else:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
                                + "&appid=7d7da9cec04671cc03ef4220ca73d0bf")
            res = json.loads(response.content)
            print(res)
            if res["cod"] != 200:
                await ctx.send("Invalid lat lon!")
                return 500
            weather = res['weather'][0]['description']
            temp = format((res['main']['temp'] - 273.15) * 1.8 + 32, '.2f')
            feels_like = format((res['main']['feels_like'] - 273.15) * 1.8 + 32, '.2f')
            humidity = format(res['main']['humidity'], '.2f')
            await ctx.send(
                f"```Here Is the weather info for {lat}, {lon}:\n    Weather: {weather}\n    Temp: {temp}f\n    Feels like: {feels_like}f\n    Humidity: {humidity}```")
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        """
        Clears all messages in a channel.
        """
        # define empty list to accumulate messages in
        mgs = []
        # accumulate messages
        async for x in ctx.channel.history():
            mgs.append(x)
        # delete all messages
        for m in mgs:
            await m.delete()
    @commands.command(pass_context=True)
    async def covid19(self, ctx):
        """
        Gets current global covid19 statistics
        :return: current covid 19 statistics according to covid19api.com
        """
        response = requests.get("https://api.covid19api.com/world/total")
        print(response.status_code)
        print(response.content)
        res = json.loads(response.content)
        confirmed = res['TotalConfirmed']
        deaths = res['TotalDeaths']
        recovered = res['TotalRecovered']
        await ctx.send(
            f"```The most recent covid19 global statistics show:\n\n"
            f"{confirmed:,} confirmed cases of covid19\n\n"
            f"{deaths:,} covid19 deaths\n\n"
            f"{recovered:,} people recovered from covid19.```")


# setup function required for cogs
def setup(client):
    client.add_cog(UtilityCog(client))
