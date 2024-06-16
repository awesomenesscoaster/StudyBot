from discord.ext import commands
import discord
import openai

class ChatGPTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    openai.api_key = 'sk-proj-gHRKR78L1jk64NcTHTfsT3BlbkFJLCnmYzbytPdKR4lmjUIF'
    
    @commands.command()
    async def chatgpt(self, ctx, *, prompt):
        await ctx.send('Processing your request...')
        
        try:
            response = openai.Completion.create(
                engine = "gpt-3.5-turbo-instruct",
                prompt = prompt,
                max_tokens = 300
            )
            answer = response["choices"][0].text.strip()
            embed = discord.Embed(
                title = f'ChatGPT',
                description= f'{answer}',
                color = discord.Color.from_rgb(255, 252, 255),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}. Command canceled.")
            
async def setup(bot):
    await bot.add_cog(ChatGPTCog(bot))