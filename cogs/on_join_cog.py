"""
This cog defines the on_member_join function to allow people to go through a registration process
TODO: comment this spaghetti
"""

from discord.ext import commands
from collections.abc import Sequence
import discord


def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)


def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)

    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True

    return check


class OnJoinCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def ask_faculty(self, member):
        await member.send("Are you a faculty member? (Y/N)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response.upper()
        if 'Y' in response:
            role = discord.utils.get(member.guild.roles, name="Faculty")
            await member.add_roles(role)
            return "faculty"
        if 'N' in response:
            role = discord.utils.get(member.guild.roles, name="Club Member")
            await member.add_roles(role)
            return "Member"
        else:
            await member.send("invalid response")
            await self.ask_faculty(member)

    async def ask_name(self, member):
        await member.send("Please respond with your first name as you would like it to appear on the server!")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        await member.edit(nick=response.content)
        return response.content

    async def ask_campus(self, member):
        await member.send("Are you a UNH Manchester, or UNH Durham student? (UNHM/UNHD)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response.upper()
        if "UNHM" in response:
            role = discord.utils.get(member.guild.roles, name="UNHM students")
            await member.add_roles(role)
            return "UNHM"
        if "UNHD" in response:
            return "UNHD"
        else:
            await member.send("Invalid response!")
            await self.ask_campus(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("Welcome to the UNHM programming club! I need to ask you a few questions to assign your"
                          "discord roles first!")
        name = await self.ask_name(member)
        mem_or_fac = await self.ask_faculty(member)
        if mem_or_fac != "faculty":
            campus = await self.ask_campus(member)
        else:
            campus = "N/A"
        with open('members.txt', 'a') as file:
            file.write(f"{name} {mem_or_fac} {campus}\n")

    @commands.command(pass_context=True)
    async def test_reg(self, ctx):
        user = ctx.message.author
        print(user)
        await self.on_member_join(user)


def setup(client):
    client.add_cog(OnJoinCog(client))


