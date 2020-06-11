import random
import re
from discord.ext import commands


class quiz(commands.Cog):

    number_regex = re.compile('[0-9]+')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['random'])
    async def roll(self, ctx):
        arguments = ctx.message.content.split()[1:]
        upper = 100
        lower = 0
        iterations = 1

        for word in arguments:
            if arguments.index(word) > 1:
                break

            if not self.number_regex.match(word):
                await ctx.message.channel.send('First 2 arguments must be integers!')
                return

        if len(arguments) >= 3 and self.number_regex.search(arguments[2]):
            iterations = int(arguments[2])
            if iterations > 10:
                await ctx.message.channel.send('Maximum number of rolls is 10')
                iterations = 10

        if arguments:
            if len(arguments) == 1:
                upper = int(arguments[0])
            else:
                lower = int(arguments[0])
                upper = int(arguments[1])

        for i in range(iterations):
            roll_result = random.randrange(lower, upper + 1)  # Adding one as roll is exclusive of last upper
            await ctx.message.channel.send(roll_result)


