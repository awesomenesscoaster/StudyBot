from discord.ext import commands
import discord
import asyncio

class QACog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def QAHelp(self, ctx):
        embed = discord.Embed(
            title = 'Q&A Help',
            description= '**!AddQ** - Ask a question to make a specific thread. \n'
            '**!ArchiveQ** - Archive a discussion about a question \n'
            '**!DeleteQ** - Delete/End the discussion on a question',
            color = discord.Color.from_rgb(245, 247, 178),
        )
        await ctx.send(embed = embed)
        
    @commands.command()
    async def AddQ(self, ctx):
        embed = discord.Embed(
            title= 'Add Question',
            description= 'What is the topic regarding your question?',
            color = discord.Color.from_rgb(245, 247, 178),
        )
        await ctx.send(embed=embed)

        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try: 
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            message_content = message.content
            embed = discord.Embed(
                title = 'Add Question',
                description= 'What question would you like to ask?',
                color = discord.Color.from_rgb(245, 247, 178),
            )
            await ctx.send(embed= embed)
            
            try:
                user_input = await self.bot.wait_for('message', check=check, timeout =15)
                user_input_content = user_input.content
                thread = await user_input.create_thread(
                    name=f'Question regarding {message_content}',
                )
                
            except asyncio.TimeoutError:
                await ctx.send('You took too long to respond. Command canceled.')
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command Canceled.')
        
    @commands.command()
    async def DeleteQ (self, ctx):
        if isinstance(ctx.channel, discord.Thread):
            await ctx.channel.delete()
            await ctx.send('The discussion has been deleted.')
        else:
            await ctx.send('This command can only be used within a thread.')
        
    @commands.command()
    async def ArchiveQ (self, ctx):
        if isinstance(ctx.channel, discord.Thread):
            await ctx.channel.edit(archived=True)
            await ctx.send('Discussion archived.')
        else:
            await ctx.send('This command can only be used within a thread.')
                
async def setup(bot):
    await bot.add_cog(QACog(bot))