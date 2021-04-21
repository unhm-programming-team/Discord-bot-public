"""
File: fun_cog.py
defines fun commands in a cog class!
Contributors: Bryan Robbins, Karl Miller
Created: 3/20/2021
Updated: 3/21/2021
"""

import random
import xkcd
from discord.ext import commands  # required for method and cog decoration
from our_packages.api_manager import getrequest
from our_packages.json_manager import count_command, easter_egg_animal_lover



class FunCog(commands.Cog):
    """
    Fun Commands Go here
    """
    def __init__(self, client):
        self.client = client


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
        # might need to do more thorough url string replacing
        # for dealing with other url unsafe characters
        url_string = msg_content.replace(' ', '%20')
        robot_img = f"https://robohash.org/{url_string}.png"
        await ctx.send(robot_img)

    @commands.command(pass_context=True, aliases=['xkcd'])
    async def getxkcd(self, ctx, comic_number):
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
            await ctx.send(f'Invalid comic number. '
                           f'Please enter a number between 0 and {xkcd.getLatestComicNum()}')



    @commands.command(pass_context=True)
    async def dog(self, ctx):
        """
        !dog

        Returns a random image of a dog
        """
        res = getrequest("https://dog.ceo/"
                         "api/breeds/image/random")  # load json response as dictionary

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
        res = getrequest("https://api.thecatapi.com/v1/images/"
                         "search?api_key=8b66f595-4a29-4254-ab12-ecfbdeb8b80f")
        res = res[0]
        cat_img = res["url"]
        await ctx.send(cat_img)
        await count_command(ctx.author.id, "cat")
        await easter_egg_animal_lover(ctx.author)


def setup(client):
    """
    Set's up the cog, required fr cogs
    :return:
    """
    client.add_cog(FunCog(client))
