"""
File: bot.py
Runs the bot and defines a couple functions
Contributors: Bryan Robbins, Karl Miller
Created: 3/20/2021
Updated: 3/21/2021
"""

from discord.ext import commands

from our_packages.key_manager import get_test
from our_packages.key_manager import get_prod


testing = False # changes weather or not the bot runs on the testing token
case_insensitivity = True # changes weather or not the bot is insensitive to case

# defines the testing and production token

testing_token = get_test()
if not testing:
    production_token = get_prod()

print(production_token)

# list of cogs, used later to load cogs
cog_list = ["fun_cog", "utility_cog", "vote_cog"]

if testing:
    client = commands.Bot(command_prefix="?", case_insensitive=case_insensitivity)  # sets the prefix used to call testing bot commands
else:
    client = commands.Bot(command_prefix="!", case_insensitive=case_insensitivity)  # sets the prefix used to call bot commands



@client.event
async def on_ready():
    """
    This runs when the bot is ready
    """
    print('Bot is ready') # prints in the console when the bot is running


for cog_item in cog_list:  # iterated through cog_list and loads them
    client.load_extension("cogs." + cog_item)  # loads cogs from cogs folder


# runs the bot using the bots token
if testing:
    client.run(testing_token)  # runs the test bot
else:
    client.run(production_token)  # runs the production bot
