import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, client):

        self.client = client
    
    @commands.command()
    async def cool(self, ctx):
        await ctx.send("Solbriller")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Ready!')



def setup(client):
    client.add_cog(Events(client))