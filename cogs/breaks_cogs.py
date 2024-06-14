from discord.ext import commands
import discord
import asyncio

class BreakIntervalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.break_sessions = {}
        
    @commands.command()
    async def BreakHelp(self,ctx):
        embed = discord.Embed(
            title = 'Break Help',
            description= '**!AddBreakTimed** - Add a break reminder for a definite amount of time \n'
            '**!BreaksOn** - Sets break reminders loop \n'
            '**!BreaksOff** - Turn off break reminders',
            color = discord.Color.from_rgb(252,167,87)
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def AddBreakTimed(self,ctx):
        embed = discord.Embed(
            title = 'Add Break Reminder',
            description= 'How long do you plan on working for? Ex: 60 for 60 minutes.',
            color = discord.Color.from_rgb(252,167,87)
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content
            work_duration = int(user_input)
            
            embed = discord.Embed(
                title= 'Add Break Reminder',
                description= 'How often would you like the reminder to be send. Ex: 20 for every 20 minutes.',
                color= discord.Color.from_rgb(252,167,87)
            )
            await ctx.send(embed=embed)
            
            try: 
                message2 = await self.bot.wait_for('message', check=check, timeout=15)
                user_input2 = message2.content
                interval_length = int(user_input2)
                
            except asyncio.TimeoutError:
                await ctx.send('You took too long to respond. Command canceled.')
            except ValueError:
                await ctx.send(f'Invalid input for **{user_input2}**. Please provide the duration in minutes. Command canceled.')
            
            await ctx.send(f'You have set a work session for **{work_duration}** minutes. \n You will receive break reminders every **{interval_length}** minutes.')
            await self.schedule_breaks(ctx, work_duration, interval_length)
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
        except ValueError:
            await ctx.send(f'Invalid input for **{user_input}**. Please provide the duration in minutes. Command canceled.')
        
        
    async def schedule_breaks(self, ctx,work_duration, interval_length):
        break_interval = interval_length
        total_breaks = work_duration // break_interval
        
        for i in range(total_breaks):
            await asyncio.sleep(break_interval * 60)
            embed = discord.Embed(
                title = 'Break Reminder',
                description= 'Time to take a break. Stretch, hydrate, and rest for a couple seconds.',
                color= discord.Color.from_rgb(252, 167, 87)
            )
            await ctx.send(embed=embed)
        
        await asyncio.sleep((work_duration % break_interval) * 60)
        embed = discord.Embed(
            title = 'Work Session Complete',
            description = f'Your **{work_duration}**-minute work session is over.',
            color=discord.Color.from_rgb(252, 167, 87)
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def BreaksOn(self,ctx):
        embed = discord.Embed(
            title= 'Break Reminder',
            description= 'How often would you like to be reminded to take a break?',
            color= discord.Color.from_rgb(252,167,87)
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout=15)
            user_input = message.content
            interval_length = int(user_input)
            
            await ctx.send(f'You have set an interval length to **{user_input}** minutes.')
            self.break_sessions[ctx.author.id] = True
            await self.start_break_loop(ctx, interval_length)
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
        except ValueError:
            await ctx.send(f'Invalid format for **{user_input}**. Please provide the duration in minutes. Command canceled.')
        
    async def start_break_loop(self, ctx, interval_length):
        while self.break_sessions.get(ctx.author.id, False):
            await asyncio.sleep(60 *interval_length)
            embed = discord.Embed(
                title= 'Break Reminder',
                description= 'Time to take a break. \n Stretch, hydrate, and relax for a few seconds.',
                color=discord.Color.from_rgb(252,167,87)
            )
            await ctx.send(embed=embed) 
        await ctx.send('Break reminders have been turned off.')
    
    @commands.command()
    async def BreaksOff(self, ctx):
        self.break_sessions[ctx.author.id] = False
        await ctx.send('Break reminders have been turned off.')
    
async def setup(bot):
    await bot.add_cog(BreakIntervalCog(bot))