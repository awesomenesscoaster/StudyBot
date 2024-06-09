from discord.ext import commands
import discord

class FlashcardsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='View', style=discord.ButtonStyle.primary, custom_id= 'viewflashcards')
    async def viewButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Test', ephemeral = True)
    
    @discord.ui.button(label = 'Add', style=discord.ButtonStyle.primary, custom_id='addflashcards')
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.server_id = interaction.guild.id
        
class FlashcardsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_embed(self, ctx):
        print('Sending embed...')
        embed = discord.Embed(
            title="Flashcards",
            description="Flashcards are an opportunity for you to review and memorize old material! \n \n" 
            "**View** - View a list of all review sets. \n"
            "**Add** - Add a flashcard set to the existing list. \n"
            "**Remove** - Remove a flashcard set from the list \n "
            "**Review** - Review/Practice with a flashcard set.",
            color=discord.Color.from_rgb(146, 197, 241),
        )
        view = FlashcardsView()
        await ctx.send(embed=embed, view=view)
        print("Embed sent")

    @commands.command()
    async def flashcards(self, ctx):
        print('Flashcard commands invoked')
        await self.send_embed(ctx)


async def setup(bot):
    await bot.add_cog(FlashcardsCog(bot))
