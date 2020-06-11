import random
from datetime import datetime, timedelta
from discord.ext import commands


class definition(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.word_dict = {}

        f = open("definitions.txt", "r")
        for line in f:
            s_line = line.split("=")
            self.word_dict[s_line[0].strip()] = s_line[1].strip()

    @commands.command()
    async def definition(self, ctx):

        if len(self.word_dict) == 0:
            print("Words exhausted or not yet loaded from definitions file.")
            return

        iterations = 1
        split_msg = ctx.message.content.split(" ")

        if len(split_msg) > 1 and str.isdigit(split_msg[1]):
            iterations = int(split_msg[1])

        for i in range(0, iterations):
            keys = list(self.word_dict.keys())
            word = keys[random.randint(0, (len(keys)) - 1)]

            await ctx.message.channel.send(f'\nDefinition : {self.word_dict.pop(word)}')
            guessed = False

            chars = [i for i in word]
            mask = ['-' for i in word]
            indices = [i for i in range(len(chars))]

            print("The word is : " + word)

            start_time = datetime.now()
            last_reveal = datetime.now()

            while not guessed:
                if datetime.now() - start_time > timedelta(seconds=180):
                    break

                if len(indices) > 0 and (datetime.now() - last_reveal) >= timedelta(seconds=10):
                    random_index = indices.pop(random.randint(0, len(indices) - 1))
                    mask[random_index] = chars[random_index]
                    await ctx.message.channel.send("".join(mask))
                    last_reveal = datetime.now()
                elif len(indices) == 0:
                    await ctx.message.channel.send(f"No one guessed the word in time, the word was {word}.")
                    break

                messages = await ctx.message.channel.history().flatten()
                new_messages = [i for i in messages if i.created_at > start_time]

                for m in new_messages:
                    if str.lower(m.content.strip()) == word and not (m.author == self.bot.user):
                        await ctx.message.channel.send(f'{m.author} guessed the word correctly!')
                        guessed = True
                        break

