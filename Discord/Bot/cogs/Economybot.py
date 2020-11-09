import discord
from discord.ext import commands
import json
import os
import random

client = commands.Bot(command_prefix = "!")

@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["balance"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    em.add_field(name = "Wallet balance", value = wallet_amt)
    em.add_field(name = "Bank balance", value = bank_amt)
    await ctx.send(embed = em)

@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} coins!")

    users[str(user.id)]["wallet"] += earnings

    with open("authentication.json","w") as f:
        json.dump(users,f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["balance"] = 0
    
    with open("authentication.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("authentication.json","r") as f:
        users = json.load(f)

    return users