from discord.ext import commands
import discord
import asyncio

class SugggestionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def Suggestion(self, ctx):
        embed = discord.Embed(
            title= 'Suggestion',
            description= 'What suggestion would you like to add?',
            color = discord.Color.from_rgb(255, 255, 255),
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 60)
            suggestion_info = message.content
            
            with open('suggestions.txt', 'a') as fhand:
                fhand.write(suggestion_info + '\n')
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
        
async def setup(bot):
    await bot.add_cog(SugggestionCog(bot))