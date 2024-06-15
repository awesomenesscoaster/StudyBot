from discord.ext import commands
import discord
import asyncio
class FlashcardsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        #flashcards : {server id: {topic : { term: answer } } }
        
    @discord.ui.button(label='View', style=discord.ButtonStyle.primary, custom_id= 'viewflashcards')
    async def viewButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Test', ephemeral = True)
    
    @discord.ui.button(label = 'Add', style=discord.ButtonStyle.primary, custom_id='addflashcards')
    async def addButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.server_id = interaction.guild.id
        
class FlashcardsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flashcards = {}

    @commands.command()
    async def FlashcardHelp(self, ctx):
        embed = discord.Embed(
            title="Flashcards",
            description= 
            "**!ViewCards** - View a list of all review sets. \n"
            "**!AddCard** - Add a flashcard set to the existing list. \n"
            "**!RemoveCard** - Remove a flashcard set from the list \n "
            "**!RemoveSet** - Remove a flashcard set from the list \n",
            color=discord.Color.from_rgb(146, 197, 241),
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def AddCard(self, ctx):          
        server_id = ctx.guild.id
        if server_id not in self.flashcards:
           self.flashcards[server_id] = {}
        
        topic_list = ''
        if not self.flashcards[server_id].items():
            embed = discord.Embed(
                title = 'Add Flashcards',
                description= 'There are no current flashcard sets. \n What would you like the topic of this set to be named?',
                color=discord.Color.from_rgb(146, 197, 241),
            )
            await ctx.send(embed=embed)
        else:
            for i in self.flashcards[server_id]:
                topic_list += '- ' + i + '\n'
            
            embed = discord.Embed(
                title = 'Add Flashcards',
                description= 'Current flashcard sets: \n' + topic_list + '\n Which topic would you like to add to? If your wanted topic is not above, write it below to add a new set.',
                color=discord.Color.from_rgb(146, 197, 241),
            )
            await ctx.send(embed=embed)
            
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
        try:
            topic_msg = await self.bot.wait_for('message', check=check, timeout = 15)
            topic = topic_msg.content
            if topic.lower() == 'exit':
                await ctx.send('Exiting flashcard addition.')
                return
            if topic not in self.flashcards[server_id]:
                self.flashcards[server_id][topic] = {}
                
            embed = discord.Embed(
                title= 'Add Flashcards',
                description= f"Adding flashcards to **{topic}**. Type 'exit' to stop. ",
                color=discord.Color.from_rgb(146, 197, 241),
            )
            await ctx.send(embed=embed)
                
            while True:
                embed = discord.Embed(
                    title= 'Add Flashcards',
                    description= 'Enter the question/term:',
                    color=discord.Color.from_rgb(146, 197, 241),
                )
                await ctx.send(embed=embed)
                    
                try:
                    question_msg = await self.bot.wait_for('message', check=check, timeout = 20)
                    question = question_msg.content
                    if question.lower() == 'exit':
                        await ctx.send('Exited flashcard addition.')
                        break
                    
                    embed = discord.Embed(
                        title= 'Add Flaschards',
                        description= f'What is the answer/definition for **{question}**',
                        color=discord.Color.from_rgb(146, 197, 241),
                    )
                    await ctx.send(embed = embed)
                        
                    try:
                        answer_msg = await self.bot.wait_for('message', check=check, timeout = 30)
                        answer = answer_msg.content
                            
                        if answer.lower() == 'exit':
                            await ctx. send('Exited flashcard addition.')
                            break
                            
                        self.flashcards[server_id][topic][question] = answer
                            
                        embed = discord.Embed(
                            title = "Add Flaschards",
                            description= f"Created new flashcard: \n {answer} answers {question}",
                            color=discord.Color.from_rgb(146, 197, 241),
                        )
                        await ctx.send(embed=embed)
                            
                    except asyncio.TimeoutError:
                        await ctx.send('You took too long to respond. Command canceled.')
                except asyncio.TimeoutError:
                    await ctx.send('You took too long to respond. Command canceled.')
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')

    @commands.command()
    async def ViewCards(self, ctx):
        server_id = ctx.guild.id
        
        if not server_id in self.flashcards:
            await ctx.send('There are no flashcard sets.')
            return

        server_topics = self.flashcards[server_id]
        
        if not server_topics:
            await ctx.send('There are no flashcard sets.')
            return

        topics_list = '\n'.join(f'- {topic}' for topic in server_topics)
        
        embed = discord.Embed(
            title= 'View Flashcards',
            description= f'Current Flashcard Sets: \n {topics_list} \n'
            'Which set would you like to view?',
            color=discord.Color.from_rgb(146, 197, 241),
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout=20)
            topic = message.content
            
            if topic not in self.flashcards[server_id]:
                raise ValueError(f'Invalid input: **{topic}**. Command canceled.')
            
            flashcard_set = ''
            for question, answer in self.flashcards[server_id][topic].items():
                flashcard_set += f'**{question}** -- {answer} \n'
            
            embed = discord.Embed(
                title= 'View Flashcards',
                description= flashcard_set,
                color=discord.Color.from_rgb(146, 197, 241),
            )
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
            
    @commands.command()
    async def RemoveSet(self,ctx):
        server_id = ctx.guild.id
        
        if not server_id in self.flashcards:
            await ctx.send('There are no flashcard sets.')
            return

        server_topics = self.flashcards[server_id]
        
        if not server_topics:
            await ctx.send('There are no flashcard sets.')
            return

        topics_list = '\n'.join(f'- {topic}' for topic in server_topics)
        
        embed = discord.Embed(
            title= 'Remove Flashcard Set',
            description= f'Current flascard sets: \n {topics_list} \n'
            'Which would you like to remove?',
            color=discord.Color.from_rgb(146, 197, 241),
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout = 20)
            chosen_topic = message.content
            
            if chosen_topic not in self.flashcards[server_id]:
                raise ValueError(f'Invalid set: **{chosen_topic}**. Command canceled.')
            
            del self.flashcards[server_id][chosen_topic]
            
            await ctx.send(f'Flashcard set for **{chosen_topic}** has been removed.')
            
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
    
    @commands.command()
    async def RemoveCard(self,ctx):
        server_id = ctx.guild.id
        
        if not server_id in self.flashcards:
            await ctx.send('There are no flashcard sets.')
            return

        server_topics = self.flashcards[server_id]
        
        if not server_topics:
            await ctx.send('There are no flashcard sets.')
            return

        topics_list = '\n'.join(f'- {topic}' for topic in server_topics)
        
        embed = discord.Embed(
            title = "Remove Flashcards",
            description= f'Current flashcard sets: \n {topics_list} \n'
            'Which set would you like to delete cards from?',
            color=discord.Color.from_rgb(146, 197, 241),
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await self.bot.wait_for('message', check=check, timeout= 20)
            topic_choice = message.content
            
            if topic_choice not in self.flashcards[server_id]:
                raise ValueError(f'Invalid set: **{topic_choice}**. Command canceled.')
            
            if not self.flashcards[server_id][topic_choice]:
                await ctx.send('There are no flashcards in this set.')
                return
            
            count = 1
            flashcards_display = ''
            for term,definition in self.flashcards[server_id][topic_choice].items():
                flashcards_display += f'{count}. **{term}** - {definition} \n'
                count += 1
            
            embed = discord.Embed(
                title= 'Remove Flashcards',
                description= flashcards_display + '\n'
                'Which flashcard (number) would you like to remove? Ex: 1',
                color = discord.Color.from_rgb(146, 197, 241),
            )
            await ctx.send(embed=embed)
        
            try:
                message = await self.bot.wait_for('message', check=check, timeout = 20)
                chosen_card = message.content
                
                if not int(chosen_card):
                    raise ValueError(f'Invalid format for **{chosen_card}**. Must be an integer value.')
                
                chosen_card = int(chosen_card)
                if chosen_card < 0 or chosen_card > len(self.flashcards[server_id][topic_choice]):
                    raise ValueError(f'Invalid format for **{chosen_card}**. Integer value must be in the given range.')
                
                question = list(self.flashcards[server_id][topic_choice].keys())[chosen_card-1]
                
                embed = discord.Embed(
                    title = 'Remove Flashcards',
                    description= 'Removing the following flashcard: \n'
                    f'**{question}** -- {self.flashcards[server_id][topic_choice][question]}',
                    color = discord.Color.from_rgb(146, 197, 241),
                )
                await ctx.send(embed=embed)
                
                del self.flashcards[server_id][topic_choice][question]
                
            except asyncio.TimeoutError:
                await ctx.send('You took too long to respond. Command canceled.')
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Command canceled.')
    
    #--------------- REVIEW COMMANDS ----------------#
    
    @commands.command()
    async def ReviewHelp(self,ctx):
        embed = discord.Embed(
            title= "Review",
            description= '**!ReviewSet** - Review the flashcards from an existing set.',
            color= discord.Color.from_rgb(199, 198, 196),
        )
        await ctx.send(embed=embed)
        
        
    
    @commands.command()
    async def ReviewSet(self, ctx):
        server_id = ctx.guild.id
        
        if not server_id in self.flashcards:
            await ctx.send('There are no flashcard sets.')
            return

        server_topics = self.flashcards[server_id]
        
        if not server_topics:
            await ctx.send('There are no flashcard sets.')
            return

        topics_list = '\n'.join(f'- {topic}' for topic in server_topics)
        
        embed = discord.Embed(
            title = "Review Set",
            description= f'Current flashcard sets: \n {topics_list} \n'
            'Which set would you like to review?',
            color=discord.Color.from_rgb(146, 197, 241),
        )
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

async def setup(bot):
    await bot.add_cog(FlashcardsCog(bot))