from discord.ext import commands
import discord
import asyncio

class To_Do_ListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ToDoLists = {}
        
        #   Todo lists{server_id: [ list of tasks to do ]}
        
    @commands.command()
    async def ToDoHelp(self,ctx):
        embed = discord.Embed(
            title = 'To-Do Help',
            description= 'Here are all the current commands available for the timer directory: \n'
            '**!AddTask** - Adds a task to the to-do list \n'
            '**!ViewTasks** - View the to-do list \n'
            '**!RemoveTask** - Remove a task from the list ',
            color= discord.Color.from_rgb(246, 138, 130),
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def AddTask(self, ctx):
        embed = discord.Embed(
            title = 'Add to To-Do List',
            description = "What task would you like to add to the to-do list?",
            color= discord.Color.from_rgb(246, 138, 130),
        )
        await ctx.send(embed = embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content
            server_id = ctx.guild.id
            self.ToDoLists.setdefault(server_id, [])
            self.ToDoLists[server_id].append(user_input)
            
            await ctx.send(f'Task: **{user_input}** has been added to the To-Do List.')
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
            
    @commands.command()
    async def ViewTasks(self, ctx):
        server_id = ctx.guild.id
        server_tasks = self.ToDoLists.get(server_id, [])
        if not server_tasks:
            await ctx.send('There are no current items in the to-do list.')
            return

        message = ''
        for task in server_tasks:
            message += f'- {task} \n'
        
        embed = discord.Embed(
            title = 'To-Do List',
            description= 'Here are the current tasks in the list: \n' + message,
            color = discord.Color.from_rgb(246, 138, 130),
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def RemoveTask(self,ctx):
        server_id = ctx.guild.id
        server_tasks = self.ToDoLists.get(server_id, [])
        
        if not server_tasks:
            await ctx.send('There are no current tasks.')
            return
        
        message = ''
        for task in server_tasks:
            message += f'- {task} \n'
        
        embed = discord.Embed(
            title = 'Remove Task',
            description= 'What task would you like to remove? \n' + message,
            color= discord.Color.from_rgb(246, 138, 130)
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        def validInput(user_input):
            return user_input in server_tasks
        
        def removeInputTask(user_input):
            del server_tasks[server_tasks.index(user_input)]
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content
            if validInput(user_input):
                removeInputTask(user_input)
                await ctx.send(f'Task: **{user_input}** has been deleted.')
                return None
            await ctx.send(f'Invalid input for **{user_input}**. Command Canceled')
            return None
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command Canceled.')
        
async def setup(bot):
    await bot.add_cog(To_Do_ListCog(bot))