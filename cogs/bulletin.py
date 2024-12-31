from discord.ext import commands
import discord
import asyncio

class BulletinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulletin = {}
    
    @commands.command()
    async def BulletinHelp(self, ctx):
        embed = discord.Embed(
            title = 'Bulletin Board Help',
            description = "test",
            color = discord.Color.from_rgb(252, 167, 87)
        )
        await ctx.send(embed = embed)
    
    @commands.command()
    async def BulletinSetup(self, ctx):
        embed = discord.Embed(
            title = "Bulletin Board Setup",
            description="Which channel would you like to indicate as the location to post your bulletin board \n \nType 'cancel' to cancel the command.\nType 'create' to have us create one for you.",
            color = discord.Color.from_rgb(252, 167, 87)
        )
        await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('channel', check=check, timeout = 15)
            user_input = message.content.strip().lower()


            if user_input == "cancel":
                await ctx.send("Command canceled.")
                return
            
            elif user_input == "create":
                embed = discord.Embed(
                    title = "Bulletin Board Setup",
                    description = "Please provide a name for the new channel.",
                    color = discord.Color.from_rgb(252,167,87)
                )
                await ctx.send(embed=embed)

                try:
                    message = await self.bot.wait_for("message", check=check, timeout=15)
                    new_channel_name = message.content.strip()

                    guild = ctx.guild
                    new_channel = await guild.create_text_channel(new_channel_name)

                    embed = discord.Embed(
                        title = "Bulletin Board Setup",
                        description= f'You indicated {user_input} as your designated channel',
                        color = discord.Color.from_rgb(252, 167, 87)
                    )
                    await ctx.send(embed=embed)

                except asyncio.TimeoutError:
                    await ctx.send("You took too long too respond. Command canceled.")

            else:
                channel = discord.utils.get(ctx.guild.text_channels, name=user_input)
                if channel:
                    embed = discord.Embed(
                        title = "Bulletin Board Setup",
                        description = f"You have set {channel.mention} as you designated bulletin board channel.",
                        color = discord.Color.from_rgb(252,167,87)
                    )
                    await ctx.send(embed=embed)

                else:
                    embed=discord.Embed(
                        title= "Bulletin Board Setup",
                        description= f"The channel {user_input} does not exist. Please try the command again.",
                        color= discord.Color.from_rgb(252,167,87)
                    )
                    await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Command canceled.")

    @commands.command()
    async def BulletinAdd(self, ctx):
        embed = discord.Embed(
            title = "Add Bulletin Post",
            description= "What would you like to add to the Bulletin Board?",
            color = discord.Color.from_rgb(252, 167, 87)
        )
        await ctx.send(embed = embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 15)
            user_input = message.content

            embed = discord.Embed(
                title = "Add Bulletin Post",
                description= f'Posting: \n \n{user_input}',
                color = discord.Color.from_rgb(252, 167, 87)
            )
            await ctx.send(embed = embed)

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. command Canceled.")


async def setup(bot):
    await bot.add_cog(BulletinCog(bot))