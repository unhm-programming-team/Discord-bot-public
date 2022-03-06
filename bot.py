"""
File: bot.py
Runs the bot and defines a couple functions
Contributors: Bryan Robbins, Karl Miller, Tony Pion
Created: 3/20/2021
Updated: 3/04/2022
"""

from discord.ext import commands
import discord
from our_packages.key_manager import get_test
from our_packages.key_manager import get_prod


intents = discord.Intents.default()
intents.members = True
TESTING = True  # changes weather or not the bot runs on the testing token
CASE_INSENSITIVITY = True  # changes weather or not the bot is insensitive to case

# defines the testing and production token

testing_token = get_test()
if not TESTING:
    production_token = get_prod()


# list of cogs, used later to load cogs
cog_list = ["fun_cog", "utility_cog", "vote_cog", "on_join_cog", "stock_cog", "faces_cog"]

if TESTING:
    client = commands.Bot(command_prefix="?",
                          case_insensitive=CASE_INSENSITIVITY,
                          intents=intents,
                          help_command=None)  # sets the prefix used to call testing bot commands
else:
    client = commands.Bot(command_prefix="!",
                          case_insensitive=CASE_INSENSITIVITY,
                          intents=intents,
                          help_command=None)  # sets the prefix used to call bot commands


for cog_item in cog_list:  # iterated through cog_list and loads them
    client.load_extension(f"cogs.{cog_item}")  # loads cogs from cogs folder

@client.event
async def on_ready():
    """
    This runs when the bot is ready
    """
    print('Bot is ready') # prints in the console when the bot is running





# runs the bot using the bots token
if TESTING:
    client.run(testing_token)  # runs the test bot
else:
    client.run(production_token)  # runs the production bot
