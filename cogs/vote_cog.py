"""
File: vote_cog.py
defines vote commands in a cog class
Contributors: Bryan Robbins, Karl Miller
Created: 3/21/2021
Updated: 3/21/2021
"""

from discord.ext import commands


class VoteCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def hostvote(self, ctx, vote_subject):
        """
        !hostvote <vote_subject>
        vote_subject = string
        Sends a message to allow currently unofficial voting on subjects
        """
        cross_emoji = "❌"
        check_emoji = "✅"

        vote_msg = await ctx.send(f"{ctx.author.name} is hosting a vote!```"
                                  f"{vote_subject}"
                                  f"```\n"
                                  f"Please click one of the reactions below to submit your vote!")
        await vote_msg.add_reaction(check_emoji)  # add check mark reaction
        await vote_msg.add_reaction(cross_emoji)  # add cross reaction


# setup function required for cogs
def setup(client):
    client.add_cog(VoteCog(client))