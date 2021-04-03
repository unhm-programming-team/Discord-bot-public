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
from our_packages.json_manager import count_command, get_count, easter_egg_animal_lover
import discord


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def coinflip(self, ctx):
        """
        Flips a coin
        :return: result of coin flip
        """
        flip = random.randint(0,1)
        if flip == 0:
            await ctx.send("Heads!")
        else:
            await ctx.send("Tails!")

    @commands.command(pass_context=True)
    async def robohash(self, ctx, msg_content):
        """
        Hashes string into robot image
        :param content: string to hash
        :param ctx: message context
        :return: image of a robot

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
        Gets an XKCD comic and returns info about it
        ;param comic_number: the number of the xkcd comic
        :return: XKCD comic link, title, alt-text, and image title
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
        Returns a random image of a dog
        :param ctx: message context
        :return: image of a dog
        """
        res = getrequest("https://dog.ceo/api/breeds/image/random")  # load json response as dictionary

        dog_img = res["message"]  # access element of res containing picture of dog
        await ctx.send(dog_img)
        await count_command(ctx.author.id, "dog")
        await easter_egg_animal_lover(ctx.author)



    @commands.command(pass_context=True)
    async def cat(self, ctx):
        """
        Returns an image of a cat
        :param ctx: message context
        :return: image of cat
        """
        res = getrequest("https://api.thecatapi.com/v1/images/search?api_key=8b66f595-4a29-4254-ab12-ecfbdeb8b80f")
        res = res[0]
        cat_img = res["url"]
        await ctx.send(cat_img)
        await count_command(ctx.author.id, "cat")
        await easter_egg_animal_lover(ctx.author)


def setup(client):
    client.add_cog(FunCog(client))