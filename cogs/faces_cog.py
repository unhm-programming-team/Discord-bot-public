"""
File: faces_cog.py
defines fun commands in a cog class!
Contributors: Bryan Robbins, Karl Miller
Created: 5/8/2021
Updated: 5/8/2021
"""
from discord.ext import commands  # required for method and cog decoration
import discord
from PIL import Image

class FacesCog(commands.Cog):
    """
    ...
    """
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def testface(self, ctx):
        await ctx.send(File=discord.File("../faces-assets/mashupv3-0.png"))


def setup(client):
    """
    Set's up the cog, required fr cogs
    :return:
    """
    client.add_cog(FacesCog(client))