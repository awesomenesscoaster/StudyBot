from discord.ext import commands
import discord
import asyncio
from datetime import datetime, timedelta

class StudyTimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timers = {}
        
    #timers = {
        #server_id: {
            #"topic 1": {"duration" : time, "start_time" : datetime.now()}...
        #}
    #}
       
    async def send_embed(self,ctx):
        embed = discord.Embed(
            title = 'Timer Help',
            description= 'Start a countdown for an event or a timer to help study. \n \n'
            'Here are all the current commands available for the timer directory: \n'
            '**StartTimer** - Starts a current timer \n'
            '**ViewTimers** - See a list of all the current timers in the server \n'
            '**ViewLiveTimer** - See a live countdown of a specific timer \n'
            '**RemoveTimer** - Remove a timer',
            color=discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed=embed)
        
    async def startTimerInstructions1(self, ctx):
        embed = discord.Embed(
            title = 'Starting Timer',
            description= 'How long would you like the timer to last for? (Ex: 10h 10m 10s) \n',
            color = discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed=embed)
    
    async def setTimerTopic(self, ctx):
            embed = discord.Embed(
                title = 'Starting Timer',
                description= 'What should this timer be labeled as?',
                color = discord.Color.from_rgb(209, 178, 243),
            )
            await ctx.send(embed = embed)
    
    @commands.command()
    async def TimerHelp(self,ctx):
        await self.send_embed(ctx)
    
    @commands.command()
    async def StartTimer(self, ctx):
        await self.startTimerInstructions1(ctx)
        
        #Check if person who sent message is same
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        #check if the input is a format we can utilize (ex: 10h 10m 1s)
        def validTime(user_input):
            time = user_input.strip()
            time = time.split()
            units = ['s', 'm', 'h']
            for i in time:
                if i[len(i)-1] not in units:
                    return False
            return True
        
        #convert the the length of time into seconds
        def durationCalculation(user_input):
            time = user_input.strip()
            time = time.split()
            duration = 0
            
            for i in time:
                value = i[:-1]
                unit = i[-1]
                if unit == 's':
                    duration += int(value)
                elif unit == 'm':
                    duration += int(value) * 60
                elif unit == 'h':
                    duration += int(value) * 3600
                    
            if duration <= 0:
                return False
            return duration
            
        #add the duration to the dictionary....
        def setTime(topic: str, duration: str):
            server_id = ctx.guild.id
            self.timers.setdefault(server_id, {})
            self.timers[server_id][topic] = {
                'duration' : duration,
                'start_time' : datetime.now()
            }
        
        #Timeout Check (15 seconds)
        try:
            message = await self.bot.wait_for('message', check = check, timeout = 15)
            user_input = message.content
            if validTime(user_input):
                duration = durationCalculation(user_input)
                if duration > 0:
                    await self.setTimerTopic(ctx)
                    
                    topic_wait = await self.bot.wait_for('message', check=check, timeout = 15)
                    topic = topic_wait.content
                    
                    setTime(topic, duration)
                    await ctx.send(f'Timer for **{topic}** set to **{duration}** seconds in this server.')
                    
                    return None
            await ctx.send(f'Invalid format for: **{user_input}**. Command Canceled.')
        except asyncio.TimeoutError:
            await ctx.send('You took to long to respond. Command canceled.')
    
    async def viewAllTimers(self, ctx):
        server_id = ctx.guild.id
        server_timers = self.timers.get(server_id, {})
        message = ''
        if not server_timers:
            await ctx.send('There are no current timers in the server.')
            return

        for topic, timer_info in server_timers.items():
            elapsed = datetime.now() - timer_info["start_time"]
            remaining = timedelta(seconds=timer_info['duration']) - elapsed
            remaining_seconds = int(remaining.total_seconds())
            minutes,seconds = divmod(remaining_seconds,60)
            message += f"**{topic}**. Time remaining: {minutes} minutes and {seconds} seconds. \n"
            
        embed = discord.Embed(
            title = 'View Timers',
            description ='\n \n' + message,
            color = discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed = embed)
            
    @commands.command()
    async def ViewTimers(self,ctx):
        await self.viewAllTimers(ctx)
    
    async def liveTimerPrompt(self,ctx):
        server_id = ctx.guild.id
        server_timers = self.timers.get(server_id, {})
        if not server_timers:
            await ctx.send('There are no current timers for the server.')
            return
        
        listoftopics = ''
        for topic in server_timers:
            listoftopics += f"**{topic}**  \n"
        
        embed = discord.Embed(
            title= 'Live Timer',
            description= 'Which timer would you like to view live for the server? \n \n' + listoftopics,
            color= discord.Color.from_rgb(209, 178, 243)
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def ViewLiveTimer(self,ctx):
        await self.liveTimerPrompt(ctx)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        def validTopic(user_input):
            server_id = ctx.guild.id
            server_timers = self.timers.get(server_id, {})
            if user_input in server_timers:
                return True
            return False   
            
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content
            if validTopic(user_input):
                await self.liveTimer(ctx, user_input)
                return None
            await ctx.send(f'Invalid topic: **{user_input}**. Command Canceled.')
        except asyncio.TimeoutError:
            await ctx.send('You took to long to respond. Command canceled.')
        
    async def liveTimer(self, ctx, topic: str):
        server_id = ctx.guild.id
        server_timers = self.timers.get(server_id, {})
        embed = discord.Embed(
            title= f'{topic} - Live Timer',
            description= '',
            color = discord.Color.from_rgb(209, 178, 243),
        )
        message = await ctx.send(embed=embed)
        
        async def updateTimer():
            while True:
                timer_info = server_timers[topic]
                elapsed = datetime.now() - timer_info['start_time']
                remaining = timedelta(seconds= timer_info['duration']) - elapsed
                remaining_seconds = int(remaining.total_seconds())
                if remaining_seconds <= 0:
                    await message.edit(embed = discord.Embed(
                        title = f"Time is Up",
                        description= f'The timer for {topic} has ended.',
                        color = discord.Color.from_rgb(209, 178, 243),
                    ))
                    break
                
                minutes,seconds = divmod(remaining_seconds, 60)
                embed.description=  f"Time remaining for **{topic}**: {minutes} minutes and {seconds} seconds."
                await message.edit(embed = embed)
                await asyncio.sleep(1)
        self.bot.loop.create_task(updateTimer())
    
    async def RemoveTimerPrompt(self, ctx):
        server_id = ctx.guild.id
        server_timers = self.timers.get(server_id, {})
        
        if not server_timers:
            await ctx.send('There are no current timers in the server.')
            return
        
        listofTopics = ''
        for i in server_timers:
            listofTopics += f"**{i}** \n"
            
        embed = discord.Embed(
            title= 'Remove Timer',
            description= 'Which timer would you like to remove? \n \n' + listofTopics,
            color = discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def RemoveTimer(self, ctx):
        await self.RemoveTimerPrompt(ctx)
       
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
       
        def validTopic(user_input):
            server_id = ctx.guild.id
            server_timers = self.timers.get(server_id, {})
            if user_input in server_timers:
                return True
            return False   
            
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content
            if validTopic(user_input):
               server_id = ctx.guild.id
               self.timers[server_id].pop(user_input)
               await ctx.send(f'Timer for **{user_input}** has been removed.')
               return None
            await ctx.send(f'Invalid topic: **{user_input}**. Command Canceled.')
        except asyncio.TimeoutError:
            await ctx.send('You took to long to respond. Command canceled.')
        
async def setup(bot):
    await bot.add_cog(StudyTimerCog(bot))