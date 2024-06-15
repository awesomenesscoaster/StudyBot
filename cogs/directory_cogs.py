from discord.ext import commands
import discord


class DirectoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def helpEmbed(self, ctx):
        embed = discord.Embed(
            title= 'Commands Directory',
            description= '**!TimerHelp** - List of all timer commands \n'
            '**!ToDoHelp** - List of all the to-do list commands \n'
            '**!QAHelp** - List of all the Q&A commands \n'
            '**!SessionsHelp** - List of all study session commands \n'
            '**!BreakHelp** - List of all break/reminder commands. \n'
            '**!FlashcardHelp** - List of all flashcard commands. \n'
            '**!ReviewHelp** - List of all commands to review/practice with flashcards',
            color= discord.Color.from_rgb(180, 244, 184)
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def Help(self, ctx):
        await self.helpEmbed(ctx)
    
async def setup(bot):
    await bot.add_cog(DirectoryCog(bot))
        