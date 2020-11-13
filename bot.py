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
    print("Cars10 is loaded and ready!")

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


    
# Checks if the useres name already is in steamid.json
async def get_steamid_data(ctx):
    with open("steamid.json","r") as f:
        users = json.load(f)

    return users


#command !addnew will add the provided steamlink to steamid.json
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
    users = await get_steamid_data(ctx.author)
    user = ctx.author

    if str(user.id) in users:
        await ctx.send("but you already have a steamlink connected to your user!")
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["SteamID"] = msg.content
        
    with open("steamid.json","w") as f:
        json.dump(users,f)
    return True


async def return_steamid(ctx):
    user = ctx.author

    data = json.load(open("steamid.json"))
    steamid = data[f"{str(user.id)}"]["SteamID"].strip("https://steamcommunity.com/profiles/")  

    return steamid

@client.command()
async def stats(ctx):
    steamid = await return_steamid(ctx)


    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid={steamid}"
    r = requests.get(url)
    data = r.json()

    total_kills = data["playerstats"]["stats"][0]["value"]
    total_death = data["playerstats"]["stats"][1]["value"]

    total_kills_headshot = data["playerstats"]["stats"][25]["value"]
    total_matches_won = data["playerstats"]["stats"][127]["value"]
    total_matches_played = data["playerstats"]["stats"][128]["value"]
    
    em = discord.Embed(title = f"{ctx.author.name}'s stats", color = discord.Color.red())
    em.set_thumbnail(url = ctx.author.avatar_url)
    em.add_field(name = "Total Kills", value = total_kills)
    em.add_field(name = "Total Death", value = total_death)
    getcontext().prec = 3
    em.add_field(name = "K/D", value = Decimal(total_kills) / Decimal(total_death))
    getcontext().prec = 4
    em.add_field(name = "HS%", value = f'{Decimal(total_kills_headshot  * 100) / Decimal(total_kills)}%')
    em.add_field(name = "Total Matches Won", value = total_matches_won)
    getcontext().prec = 4
    em.add_field(name = "Win %", value = f'{Decimal(total_matches_won * 100) / Decimal(total_matches_played)}%')
    await ctx.send(embed = em)
    
@client.command()
async def lastmatch(ctx):
    steamid = await return_steamid(ctx)
    
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid={steamid}"
    r = requests.get(url)
    data = r.json()

    last_match_wins = data["playerstats"]["stats"][89]["value"]
    last_match_kills = data["playerstats"]["stats"][91]["value"]
    last_match_deaths = data["playerstats"]["stats"][92]["value"]
    last_match_mvps = data["playerstats"]["stats"][93]["value"]
    
    Win = 16
    Lose = 14
    Draw = 15
  
    if str(last_match_wins <= Lose):
        last_result = "Lose"
    if str(last_match_wins == Win):
        last_result = "Win"
    if str(last_match_wins == Draw):
        last_result = "Draw"
        
    em = discord.Embed(title = f"{ctx.author.name}'s last match", color = discord.Color.red())
    em.set_thumbnail(url = ctx.author.avatar_url)
    em.add_field(name = "Kills", value = last_match_kills)
    em.add_field(name = "Death", value = last_match_deaths)
    getcontext().prec = 3
    em.add_field(name = "K/D", value = Decimal(last_match_kills) / Decimal(last_match_deaths))   
    em.add_field(name = "MVP", value = last_match_mvps)
    em.add_field(name = "Result", value = last_result)
    await ctx.send(embed = em)    



client.run(TOKEN)