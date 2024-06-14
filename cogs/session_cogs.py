from discord.ext import commands
import discord
import asyncio
from datetime import datetime,timedelta

class SessionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #events = { server_id = { session name : time start }  }
        
    @commands.command()
    async def SessionsHelp(self, ctx):
        embed = discord.Embed(
            title = 'Study Session Help',
            description = '**!StartSession** - Start a study session at a specific time. \n'
            '**!StartSessionNow** - Start a study session instantaneously.',
            color= discord.Color.from_rgb(249, 175, 230)
        )
        await ctx.send(embed = embed)
        
    @commands.command()
    async def StartSession(self, ctx):
        embed = discord.Embed(
            title = 'Start Study Session',
            description= 'What is the name of the study session?',
            color= discord.Color.from_rgb(249, 175, 230)
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try: 
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            session_name = message.content
            
            embed = discord.Embed(
                title = 'Start Study Session',
                description= "What time would you like the study session to start? Ex: 11:55 am",
                color = discord.Color.from_rgb(249, 175, 230)
            )
            await ctx.send(embed=embed)
            
            try: 
                message = await self.bot.wait_for('message', check=check, timeout=15)
                user_input = message.content
                
                start_time = self.parse_time(user_input)
                if start_time:
                    await ctx.send(f'Study session **{session_name}** has been scheduled to start at {start_time.strftime("%I:%M:%p")}')
                    self.schedule_session(ctx.channel, session_name, start_time)
                else:
                    await ctx.send(f'Invalid format for **{user_input}**. Command canceled.')
            
            except asyncio.TimeoutError:
                await ctx.send('You took too long to respond. Command canceled')
                    
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
        
    def parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, '%I:%M %p').replace(year= datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        except ValueError:
            return None 
            
    def schedule_session(self, channel, session_name, start_time):
        now = datetime.now()
        delay = (start_time-now).total_seconds()
        self.bot.loop.create_task(self.notify_session_start(channel, session_name, delay))
        
    async def notify_session_start(self, channel, session_name, delay):
        await asyncio.sleep(delay)
        embed = discord.Embed(
        title = 'Study Session Started',
            description= f'The study session for **{session_name}** has started!',
            color = discord.Color.from_rgb(249, 175, 230)
        )
        await channel.send(embed=embed)
    
    @commands.command()
    async def StartSessionNow(self,ctx):
        embed = discord.Embed(
            title= 'Start Study Session',
            description= 'What is the topic of the session?',
            color = discord.Color.from_rgb(249, 175, 230)
        )
        await ctx.send(embed = embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check = check, timeout = 15)
            user_input = message.content
            embed = discord.Embed(
                title = 'Session Started',
                description= f'A study session for **{user_input}** has begun.',
                color = discord.Color.from_rgb(249, 175, 230)
            )
            await ctx.send(embed = embed)
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
            
async def setup(bot):
    await bot.add_cog(SessionsCog(bot))