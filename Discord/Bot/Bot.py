import discord
from discord.ext import commands
import json
import os
import requests
from decimal import *

os.chdir("C:\\Users\\Simon\\Discord\\Bot\\cogs")

client = commands.Bot(command_prefix = "!")

TOKEN ="NzczNjU1NzgwMTMzMDQ0MzA0.X6MZFw.DPbuEVVrS2UM7TVB4Y0siB4NdOQ"

cogs = ['cogs.events', 'cogs.utils']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(f"Could not load cog {cog}: {str(e)}")

# Tells when bot is loaded
@client.event
async def on_ready():
    print("Bot is ready!")

# Command !loadcog to load cogs
@client.command()
async def loadcog(ctx, cogname = None):

    if cogname is None:
        return
    
    try:
        client.load_extension(cogname)
    except Exception as e:
        print(f"Could not load cog {cogname}: {str(e)}")
    else:
        print("Loaded Cog Succesfully")

# Command !unloadcog to unload cogs
@client.command()
async def unloadcog(ctx, cogname = None):

    if cogname is None:
        return
    
    try:
        client.unload_extension(cogname)
    except Exception as e:
        print(f"Could not unload cog {cogname}: {str(e)}")
    else:
        print("Unloaded Cog Succesfully")


    

async def get_auth_data(ctx):
    with open("authentication.json","r") as f:
        users = json.load(f)

    return users



@client.command()
async def addnew(ctx):
    await ctx.send(f"Please provide your steamlink!")

    #checks if the message contains
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
        str(msg.content.lower()).startswith("https://steamcommunity.com/profiles/")

    msg = await client.wait_for("message", check=check)
    if str(msg.content.lower()).startswith("https://steamcommunity.com/profiles/"):
        await ctx.send("Thanks!")
   
    
    #checks if the user is in json file. If not add the user message to the file.
    users = await get_auth_data(ctx.author)
    user = ctx.author

    if str(user.id) in users:
        await ctx.send("but you already have a steam profile connected to your user!")
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["SteamID"] = msg.content
        
    with open("authentication.json","w") as f:
        json.dump(users,f)
    return True


@client.command()
async def stats(ctx):

    
    url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid=76561197972966230"
    r = requests.get(url)
    data = r.json()

    total_kills = data["playerstats"]["stats"][0]["value"]
    total_death = data["playerstats"]["stats"][1]["value"]
    
    total_time_played = data["playerstats"]["stats"][2]["value"]
    total_kills_headshot = data["playerstats"]["stats"][25]["value"]
    
    em = discord.Embed(title = f"{ctx.author.name}'s stats", color = discord.Color.red())
    em.add_field(name = "Total Kills", value = total_kills)
    em.add_field(name = "Total Death", value = total_death)
    getcontext().prec = 3
    em.add_field(name = "K/D", value = Decimal(total_kills) / Decimal(total_death))
    getcontext().prec = 4
    em.add_field(name = "HS%", value = Decimal(total_kills_headshot  * 100) / Decimal(total_kills)"%")
    em.add_field(name = "Total time played", value = total_time_played)
    await ctx.send(embed = em)
    
    



client.run(TOKEN)