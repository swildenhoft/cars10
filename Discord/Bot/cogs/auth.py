import discord
from discord.ext import commands
import json
import os
import random

os.chdir("C:\\Users\\Simon\\Discord\\Bot")

class Auth(commands.Cog):

    def __init__(self, client):

        self.client = client

    async def get_auth_data(self):
            with open("authentication.json","r") as f:
                users = json.load(f)

            return users

    

    async def on_message(self, msg, ctx):
        if msg.author == self.user:
            return

        if msg.content.startswith("https://steamcommunity.com/profiles/"):
            await ctx.process_commands(message) # add this if also using cmd decorators
                if msg.channel.id == THEIR_CHANNEL_ID_HERE:
                    target_channel = ctx.get_channel(YOUR_ANNOUNCEMENT_CHANNEL_ID_HERE)
                    await target_channel.send(msg.content)

             
        

    @commands.command()
    async def steamid(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_auth_data()

        
        bank_amt = users[str(user.id)]["SteamID"]

        em = discord.Embed(title = f"{ctx.author.name}'s SteamID", color = discord.Color.red())
        em.add_field(name = "SteamID", value = bank_amt)
        await ctx.send(embed = em)

    @commands.command()
    async def beg(self, ctx):
        await self.open_account(ctx.author)

        users = await self.get_auth_data()

        user = ctx.author

        earnings = 0

        await ctx.send(f"Someone gave you {earnings} coins!")

        users[str(user.id)]["SteamID"] = earnings

        with open("authentication.json","w") as f:
            json.dump(users,f)

    
    async def open_account(self, user):

        users = await self.get_auth_data()
        

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["SteamID"]
        
        with open("authentication.json","w") as f:
            json.dump(users,f)
        return True

    






def setup(client):

    client.add_cog(Auth(client))