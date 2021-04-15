"""
This cog defines the on_member_join function to allow people to go through a registration processg
"""

from discord.ext import commands
from collections.abc import Sequence
import discord
import requests
import json
from our_packages.json_manager import count_command, get_count, easter_egg_animal_lover

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

    async def ask_purpose(self,member ):
        """
        Request member/nonmember
        """
        await member.send("Are you a student or faculty who intends to be an active part of the club? (Y/N) (Answer No "
                          "if you are here to collaborate with the club on events, and are not a faculty member. "
                          "Otherwise answer yes)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response = response.upper()
        if "Y" in response:
            return True
        if "N" in response:
            role = discord.utils.get(member.guild.roles, name="non-member")
            await member.add_roles(role)
            return False
        else:
            await member.send(
                "Are you a student who intends to be a member, or faculty who intends to be an active part of the club? (Y/N) (Answer No"
                "if you are here to collaborate with the club on events, or some other non-member position, and are not a faculty member. Otherwise"
                "answer yes)")
            await self.ask_purpose(member)

    async def ask_faculty(self, member):
        """
        Request faculty info
        """
        await member.send("Are you a faculty member? (Y/N)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response = response.upper()
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

    async def rem_roles(self, member):
        """
        Remove all member roles that we can
        :param member:
        :return:
        """
        available_roles = ['Faculty', 'Club Member', 'UNHM students', 'non-member']
        for r in available_roles:
            role = discord.utils.get(member.guild.roles, name=r)
            try:
                await member.remove_roles(role)
            except:
                pass

    async def ask_github(self, member):
        """
        Request github username
        """
        await member.send("Please respond with your github username!")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        return response.content

    async def ask_name(self, member):
        """
        Request Name Info
        """
        await member.send("Please respond with your first name as you would like it to appear on the server!")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        await member.edit(nick=response.content)
        return response.content

    async def ask_campus(self, member):
        """
        request campus info
        """
        await member.send("Are you a UNH Manchester, or UNH Durham student? (UNHM/UNHD)")
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response = response.upper()
        if "UNHM" in response:
            role = discord.utils.get(member.guild.roles, name="UNHM students")
            await member.add_roles(role)
            return "UNHM"
        if "UNHD" in response:
            return "UNHD"
        else:
            await member.send("Invalid response!")
            await self.ask_campus(member)

    async def send_rules(self, member):
        await member.send('''Welcome to the Programming Club!/n/n

Make sure to follow our conduct rules on club communication channels:/n
- No harassment or sexualized speech /n
- No talking about politics except in specific off-topic spaces/n
- No discrimination /n
- No bullying and mocking, including and especially about someone being an inexperienced programmer/n

We have yet to have anyone come close to running afoul of these rules - this is a welcoming and inclusive space for programmers of all backgrounds and skill levels. Help us keep it that way!/n
Please reply with "Agree" if you agree with these rules''')
        response = await self.client.wait_for('message', check=message_check(member.dm_channel))
        response = response.content
        response = response.upper()
        if "AGREE" in response:
            pass
        else:
            await member.send("Invalid response!")
            await self.send_rules(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Runs on member join, asks them various questions about their position in the club
        """
        if member.guild.name != "UNHM Programming Club":
            return 200
        times_registered = await get_count(member.id, "registration")
        if times_registered > 0:
            await member.send("Warning this will clear all your roles, do you want to proceed? (Y/N)")
            response = await self.client.wait_for('message', check=message_check(member.dm_channel))
            response = response.content
            response = response.upper()
            if "N" in response:
                return 200
        await self.send_rules(member)
        await self.rem_roles(member)
        purpose = await self.ask_purpose(member) #ask their purpose, non-member/member
        name = await self.ask_name(member) # ask for name
        if purpose: # if they are a member
            mem_or_fac = await self.ask_faculty(member) # are they faculty or student?
            if mem_or_fac != "faculty": # if their not faculty
                campus = await self.ask_campus(member) # get their campus
            else:
                campus = "N/A" # if their faculty campus is not applicable
            github = await self.ask_github(member) # ask for github
            with open('members.txt', 'a') as file: # save this info to a text file
                file.write(f"Name: {name} Github: {github} , {mem_or_fac}, Campus: {campus}\n")
            embed = { # create an embed message as json
                "description": f"Name: {name}\nRole: {mem_or_fac}\nCampus: {campus}\nGithub: {github}",
                "title": "New Member"
            }

            data = { # form the rest of the message and define bot name as json
                "content": f"New Member!",
                "username": "New Member Bot",
                "embeds": [
                    embed
                ],
            }

            result = requests.post("https://discord.com/api/webhooks/826631969701625906/vfIcKFbeLnBdJD1hFS6tsuPrCWArDb4sv38O8piWgccRLqIxdovE6rsUyDn5Rw4JRsJE", json=data) # send webhook request
            try: # all of this is for debugging
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))
        else: # if their a non- member
            # form the discord embed message as json
            embed = {
                "description": f"Name: {name}",
                "title": "New Non-Member"
            }

            data = {
                "content": f"New Non-Member Info",
                "username": "New Non-Member Bot",
                "embeds": [
                    embed
                ],
            }
            # send discord message
            result = requests.post("https://discord.com/api/webhooks/826631969701625906/vfIcKFbeLnBdJD1hFS6tsuPrCWArDb4sv38O8piWgccRLqIxdovE6rsUyDn5Rw4JRsJE", json=data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Payload delivered successfully, code {}.".format(result.status_code))
        await member.send("Thank you for completing registration!") # tell them registration is complete
        await count_command(member.id, "registration")

    @commands.command(pass_context=True)
    async def manual_reg(self, ctx):
        """
        !manual_reg

        Manually start registration for yourself in case of bot error, REMOVES ALL REGISTRATION ASSIGNED ROLLS
        """
        user = ctx.message.author
        print(user)
        await self.on_member_join(user)

    @commands.command(pass_context=True)
    async def get_registered(self, ctx):
        """
        !get_registered

        return all registered members from text file
        """
        with open('members.txt', 'r') as file:
            lines = file.readlines()
        message_str = ""
        for line in lines:
            message_str += f"{line}\n"
        await ctx.send(f"```{message_str}"
                       f"```")


def setup(client):
    client.add_cog(OnJoinCog(client))


