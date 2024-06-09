from discord.ext import commands
import discord
import asyncio

class StudyTimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

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
            '**StartTimer** - Starts a current timer',
            color=discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed=embed)
        
    async def startTimerInstructions1(self, ctx):
        embed = discord.Embed(
            title = 'Starting Timer...',
            description= 'How long would you like the timer to last for? (Ex: 10h 10m 10s) \n',
            color = discord.Color.from_rgb(209, 178, 243),
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def TimerHelp(self,ctx):
        await self.send_embed(ctx)
    
    @commands.command()
    async def StartTimer(self, ctx):
        await self.startTimerInstructions1(ctx)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        def validTime(user_input):
            time = user_input.strip()
            time = time.split()
            units = ['s', 'm', 'h', 'sec', 'min', 'hour', 'seconds', 'secs', 'mins', 'minutes', 'hours']
            for i in time:
                if i[len(i)-1] not in units:
                    return False
            return True
            
        #Timeout Check (15 seconds)
        try:
            message = await self.bot.wait_for('message', check = check, timeout = 15)
            user_input = message.content
            if validTime(user_input):
                await ctx.send(f'{True}')
                return None
            await ctx.send(f'Invalid format for: **{user_input}**. Command Canceled.')
        except asyncio.TimeoutError:
                ctx.send('You took to loong to respond. Command canceled.')
        
        
async def setup(bot):
    await bot.add_cog(StudyTimerCog(bot))