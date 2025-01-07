# from discord.ext import commands, tasks
# import discord
# from dataclasses import dataclass

# CHANNEL_ID = 1248046073889689652

# @dataclass
# class Session:
#     is_active: bool = False
#     start_time: int = 0
    

# bot = commands.Bot(command_prefix= "!", intents=discord.Intents.all())
# session = Session()



# @bot.event
# async def on_ready():
#     print('Hello! Study bot is ready!')
#     channel = bot.get_channel(CHANNEL_ID)
#     await channel.send('Hello! Study bot is ready!')
    
# @bot.command()
# async def hello(ctx):
#     await ctx.send('Hello!')
    
# @bot.command()
# async def add(ctx, x, y):
#     result = int(x) + int(y)
#     await ctx.send(result)

# @bot.command()
# async def start(ctx):
#     if session.is_active: 
#         await ctx.send("A session is already active!")
#         return

#     session.is_active = True
#     session.start_time = ctx.message.created_at.timestamp()
#     await ctx.send(f'New session started at {ctx.message.created_at}')

# bot.run(BOT_TOKEN)