import discord
from discord.ext import commands
import random
class Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='$')
    async def ai(self,ctx,*,msg):
        embed = discord.Embed(color=discord.Colour.gold(),description=random.Random(msg.__hash__()).choice(await self.bot.read_json('ai.json')))
        embed.set_footer(text=f'Invoced by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='force')
    @commands.is_owner()
    async def force(self,ctx,*,phrase):

        l = await self.bot.read_json('ai.json')
        l.append(phrase)
        await self.bot.write_json('ai.json',l)
        await ctx.send(await self.bot.read_json('ai.json'))        





def setup(bot):
    bot.add_cog(Cog(bot))