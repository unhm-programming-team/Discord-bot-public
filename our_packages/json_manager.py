import json
import discord

## this spaghetti really needs some docstrings

async def count_command(user, command):
    user = str(user)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if command not in loaded_data[user].keys():
        loaded_data[user][command] = 1
    else:
        loaded_data[user][command] += 1
    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)


async def get_crypto(user):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "crypto" not in loaded_data[user].keys():
        loaded_data[user]["crypto"] = {}
    stocks = loaded_data[user]["crypto"]

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)

    return stocks


async def add_crypto(user, crypto, amt):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "crypto" not in loaded_data[user].keys():
        loaded_data[user]["crypto"] = {}
    if crypto not in loaded_data[user]["crypto"]:
        loaded_data[user]["crypto"][crypto] = 0
    loaded_data[user]["crypto"][crypto] += amt

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)


async def rem_crypto(user,crypto,amt):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "crypto" not in loaded_data[user].keys():
        loaded_data[user]["crypto"] = {}

    loaded_data[user]["crypto"][crypto] -= amt

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)



async def get_stocks(user):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "stocks" not in loaded_data[user].keys():
        loaded_data[user]["stocks"] = {}
    stocks = loaded_data[user]["stocks"]

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)

    return stocks

async def add_stock(user, stock, amt):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "stocks" not in loaded_data[user].keys():
        loaded_data[user]["stocks"] = {}
    if stock not in loaded_data[user]["stocks"]:
        loaded_data[user]["stocks"][stock] = 0
    loaded_data[user]["stocks"][stock] += amt

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)

async def rem_stock(user,stock,amt):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "stocks" not in loaded_data[user].keys():
        loaded_data[user]["stocks"] = {}

    loaded_data[user]["stocks"][stock] -= amt

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)


async def get_balance(user):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "balance" not in loaded_data[user].keys():
        loaded_data[user]["balance"] = 1000

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)

    return loaded_data[user]["balance"]

async def check_stocks(user):
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "stocks" not in loaded_data[user].keys():
        loaded_data[user]["stocks"] = {}
        return False
    amt_of_stock = 0.0
    for stock in loaded_data[user]["stocks"].keys():
        amt_of_stock += loaded_data[user]["stocks"][stock]
    if amt_of_stock == 0:
        return False
    else:
        return True


async def add_to_balance(user, balance):
    user = str(user.id)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)

    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if "balance" not in loaded_data[user].keys():
        loaded_data[user]["balance"] = 1000

    loaded_data[user]["balance"] += balance
    if 100 >= loaded_data[user]["balance"]:
        if not await check_stocks(user):
            loaded_data[user]["balance"] += 500

    with open('command_count.txt', 'w+') as file2:
        print(loaded_data)
        file2.truncate()
        json.dump(loaded_data, file2)


async def get_count(user, command):
    user = str(user)
    with open('command_count.txt', 'r') as file:
        line = str(file.readline())

    loaded_data = json.loads(line)
    if user not in loaded_data.keys():
        loaded_data[user] = {}
    if command not in loaded_data[user].keys():
        return 0
    return int(loaded_data[user][command])


async def easter_egg_animal_lover(user):
    animal_call_count = await get_count(user.id, "dog") + await get_count(user.id, "cat")
    if animal_call_count >= 50:
        role = discord.utils.get(user.guild.roles, name="Animal Lover")
        if role not in user.roles:
            await user.add_roles(role)
