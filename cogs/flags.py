from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
import random
from discord import File
from discord.ext import commands
from definitions import FLAGS_DIR


class flags(commands.Cog):

    flag_files = [f for f in listdir(FLAGS_DIR) if isfile(join(FLAGS_DIR, f))]

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def flag_path_to_name(path: str) -> str:
        return path.replace(".gif", "").replace("_", " ")

    @commands.command()
    async def flags(self, ctx):

        iterations = 1
        split_msg = ctx.message.content.split(" ")

        if len(split_msg) > 1 and str.isdigit(split_msg[1]):
            iterations = int(split_msg[1])

        for i in range(0, iterations):
            start_time = datetime.now()
            guessed = False

            random_flag_path = self.flag_files.pop(random.randint(0, len(self.flag_files) - 1))
            await ctx.message.channel.send(file=File(open(FLAGS_DIR + random_flag_path, "rb")))
            flag_string = self.flag_path_to_name(random_flag_path)
            print(flag_string)

            while not guessed:
                messages = await ctx.message.channel.history().flatten()
                new_messages = [i for i in messages if i.created_at > start_time]

                for m in new_messages:
                    if str.lower(m.content.strip()) == str.lower(flag_string) and not (m.author == self.bot.user):
                        await ctx.message.channel.send(f'{m.author.display_name} answered correctly')
                        guessed = True
                        break

                if (datetime.now() - start_time) > timedelta(seconds=15):
                    break

            if not guessed:
                await ctx.message.channel.send(f"No one has guessed the country in time, it was {flag_string}.")

