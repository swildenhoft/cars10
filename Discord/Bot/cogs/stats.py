import discord
from discord.ext import commands

class Utils(commands.Cog):

    def __init__(self, client):

        self.client = client

    @commands.command()
    async def userinfo(self, ctx, user: discord.User = None):

        if user is None:
            await ctx.send('Please provide a user to gety info on!')
            return
     
        embed = discord.Embed(title = 'Userinfo', description = f'Here is some information about {user.name}', colour = discord.Color.blue())

        embed.add_field(name = user, value = f'- User\'s name: {user.name}\n- User\'s ID: {user.id}\n- User\'s discrim: {user.discriminator}\n- User is a bot: {user.bot}')

        embed.set_thumbnail(url = user.avatar_url)

        await ctx.send(embed = embed)


def setup(client):

    client.add_cog(Utils(client))