import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix= "!", intents=discord.Intents.all())

async def on_ready():
    print(f'Logged in as {bot.user}')

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
@bot.event
async def on_ready():
    await load_cogs()
    
bot.run('#######################################')