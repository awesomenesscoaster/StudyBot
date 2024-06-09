from discord.ext import commands
import discord

class DirectoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def Help(self, ctx):
        await ctx.send('Test')
    
async def setup(bot):
    await bot.add_cog(DirectoryCog(bot))
        