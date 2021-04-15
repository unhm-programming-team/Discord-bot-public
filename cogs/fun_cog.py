"""
File: fun_cog.py
defines fun commands in a cog class!
Contributors: Bryan Robbins, Karl Miller
Created: 3/20/2021
Updated: 3/21/2021
"""

import xkcd
from our_packages.api_manager import getrequest
import random
from discord.ext import commands  # required for method and cog decoration
from our_packages.json_manager import count_command, get_count, easter_egg_animal_lover, get_balance, add_to_balance, get_stocks, add_stock, rem_stock
import requests
import time
import asyncio
import discord


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def paperbuy(self,ctx,stock, money):
        """
        !paperbuy <stock> <amt_of_money>
        Used for trading fake money on stocks!
        stock = string, stock to buy
        amt_of_money = integer
        """
        money = float(money)
        if await get_balance(ctx.author) >= money:
            price = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            num_of_stocks = money/price
            await ctx.send(f"{num_of_stocks} stocks of {stock} purchased for ${money}, at a price of ${price} per share.")

            await add_stock(ctx.author, stock, num_of_stocks)
            await add_to_balance(ctx.author, -1 * money)
        else:
            await ctx.send(f"Your balance is too low! It is currently ${await get_balance(ctx.author)}")

    @commands.command(pass_context=True)
    async def value(self,ctx, stock = None):
        """
        !value stock

        stock (optional): string, if passed returns current price of specific stock

        Shows the value of the stocks you are holding
        """
        if not stock:
            amount_of_stock = await get_stocks(ctx.author)
            message = "You are currently Holding:```"
            for stock in amount_of_stock.keys():
                if amount_of_stock[stock] != 0.0:
                    price = requests.get(
                        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
                    price = float(price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
                    message += f"{stock} worth of ${price * amount_of_stock[stock]}\n"
            message += "```"
            await ctx.send(message)
        else:
            price = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(
                price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            await ctx.send(f"The price of {stock} is currently ${price}")

    @commands.command(pass_context=True)
    async def papersell(self,ctx,stock,amt):
        """
        !papersell <stock> <amt_of_stock>

        Sell fake stocks!
        stock = string, stock to sell
        amt_of_stock = integer, amount of stock to sell
        """
        amount_of_stock = await get_stocks(ctx.author)
        amount_of_stock = amount_of_stock[stock]
        if amount_of_stock >= float(amt):
            price = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            gain_loss = float(amt) * price
            await ctx.send(f"@{ctx.author.name} you sold {amt} shares of {stock}, at a price of ${price} per share, for ${gain_loss}")
            await rem_stock(ctx.author, stock, float(amt))
            await add_to_balance(ctx.author, gain_loss)
        else:
            await ctx.send(f"You are not currently holding that much stock! You have {amount_of_stock} stocks in {stock}")

    @commands.command(pass_context=True)
    async def portfolio(self,ctx):
        """
        !portfolio

        Shows you all stocks you currently hold with the paper trading functionality.
        """
        amount_of_stock = await get_stocks(ctx.author)
        message = "You are currently Holding:```"
        for stock in amount_of_stock.keys():
            if amount_of_stock[stock] != 0.0:
                message += f"{amount_of_stock[stock]} shares of {stock}\n"
        message += "```"
        await ctx.send(message)




    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """
        !balance

        Shows current server fake money balance.
        """
        await ctx.send(f"Your balance is currently ${await get_balance(ctx.author)}")



    @commands.command(pass_context=True)
    async def coinflip(self, ctx):
        """
        !coinflip

        Flips a coin
        """
        flip = random.randint(0,1)
        if flip == 0:
            await ctx.send("Heads!")
        else:
            await ctx.send("Tails!")

    @commands.command(pass_context=True)
    async def robohash(self, ctx, msg_content):
        """
        !robohash <msg>

        Hashes msg into robot image
        msg = string

        TODO: parse string to replace unsafe characters
        """
        # not sure how to test!
        # might need to do more thorough url string replacing for dealing with other url unsafe characters
        url_string = msg_content.replace(' ', '%20')
        robot_img = f"https://robohash.org/{url_string}.png"
        await ctx.send(robot_img)

    @commands.command(pass_context=True, aliases=['xkcd'])
    async def getXKCD(self, ctx, comic_number):
        """
        !getxkcd <comic_num>

        Gets an XKCD comic comic_num and returns various info about it.

        comic_num = integer
        """
        if -1 < int(comic_number) < xkcd.getLatestComicNum(): # check for valid XKCD comic
            # get info about XCKD comic
            comic = xkcd.getComic(comic_number)
            comic_link = comic.getImageLink()
            alt_text = comic.getAltText()
            comic_name = comic.getImageName()
            comic_title = comic.getTitle()
            await ctx.send(f'```'
                           f'Here is XKCD comic {comic_number}\nTitle: {comic_title}'
                           f'```')
            await ctx.send(comic_link)
            await ctx.send(f'```'
                           f'Alternate text: {alt_text}\nImage file name: {comic_name} '
                           f'```')
        else:
            await ctx.send(f'Invalid comic number. Please enter a number between 0 and {xkcd.getLatestComicNum()}')



    @commands.command(pass_context=True)
    async def dog(self, ctx):
        """
        !dog

        Returns a random image of a dog
        """
        res = getrequest("https://dog.ceo/api/breeds/image/random")  # load json response as dictionary

        dog_img = res["message"]  # access element of res containing picture of dog
        await ctx.send(dog_img)
        await count_command(ctx.author.id, "dog")
        await easter_egg_animal_lover(ctx.author)



    @commands.command(pass_context=True)
    async def cat(self, ctx):
        """
        !cat

        Returns an image of a cat
        """
        res = getrequest("https://api.thecatapi.com/v1/images/search?api_key=8b66f595-4a29-4254-ab12-ecfbdeb8b80f")
        res = res[0]
        cat_img = res["url"]
        await ctx.send(cat_img)
        await count_command(ctx.author.id, "cat")
        await easter_egg_animal_lover(ctx.author)


def setup(client):
    client.add_cog(FunCog(client))