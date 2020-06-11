import html
import json
import random
import re
import requests
from discord.ext import commands
from scrapers.util import sleep_until

# TODO: Endless mode
# TODO: Extra questions for tie-breakers


class quiz(commands.Cog):

    valid_question_regex = re.compile('[a-dA-D]{1}\.? ?')
    question_api = 'https://opentdb.com/api.php?amount=PLACEHOLDER&category=9&type=multiple'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    letters = ['A', 'B', 'C', 'D']

    def __init__(self, bot):
        self.bot = bot
        self.answer_map = {}
        self.score_map = {}
        self.participants = []
        self.active = False

    @staticmethod
    def convert_string(raw_string) -> str:
        return raw_string.replace("&quot;", '"').replace('&#039;', "'")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if self.bot.user == msg.author:
            return

        if self.active:
            user = msg.author

            if user in self.answer_map.keys() and False:
                await msg.channel.send(f'You ({user}) have already voted for this question')
            else:
                # if not self.valid_question_regex.match(msg.content.strip()):
                #     ##await ctx.message.channel.send('On-going  ')
                #     return

                if not self.valid_question_regex.search(msg.content):
                    print("Invalid format! " + msg.content)

                if user in self.participants and self.valid_question_regex.search(msg.content):
                    letter = self.valid_question_regex.search(msg.content).group(0).replace(".", '').lower()
                    self.answer_map[user] = self.alpha.index(letter)

    @commands.group(name='quiz', invoke_without_command=True)
    async def quiz(self, ctx):

        if self.active:
            print("Quiz already active!")
            return

        questions = 5
        split_msg = ctx.message.content.split(" ")

        if len(split_msg) > 1 and str.isdigit(split_msg[1]):
            questions = int(split_msg[1])

        question_response_content = requests.get(self.question_api.replace('PLACEHOLDER', str(questions))).content
        question_json = json.loads(question_response_content)
        author_voice = ctx.author.voice  # Check if the person is in a voice channel

        if not author_voice:    # User not in voice channel
            await ctx.message.channel.send('Must be in a voice channel to use this command')
            return

        self.participants = [u for u in author_voice.channel.members]
        self.score_map = {p: 0 for p in author_voice.channel.members}
        self.active = True

        for question_number, qjs in enumerate(question_json['results']):
            if not self.active:
                return

            self.answer_map.clear()
            question_text = html.unescape(qjs['question'])              ##   self.convert_string(qjs['question'])
            correct_answer = html.unescape(qjs['correct_answer'])       ##   TODO: Recursively apply this (unescape) function to JSON dict
            possible_answers = html.unescape(qjs['incorrect_answers'])
            correct_index = random.randint(0, 3)
            possible_answers.insert(correct_index, correct_answer)

            msg = f"\n\nQuestion {str(question_number + 1)} : {question_text} \n\n"
            for c, letter in enumerate(self.letters):
                msg += f"{letter}. {html.unescape(possible_answers[c])}\n"
            msg += '\n\n'

            await ctx.message.channel.send(msg)
            await sleep_until(10, self.all_voted)

            if self.active:
                answer_message = f'\nThe correct answer is: {correct_answer} ({self.letters[correct_index]}) \n\n'
                correct = []

                for p in self.participants:
                    if p in self.answer_map and self.answer_map[p] == correct_index:
                        correct.append(p)
                        self.score_map[p] += 1

                await ctx.message.channel.send(answer_message)

        highest_score = max(self.score_map.values())

        if highest_score:
            winners = list(filter(lambda i: i[1] == highest_score, self.score_map.items()))
            winner_string = " ,".join([s[0].display_name for s in winners])

            msg = f'Winner{"s" if len(winners)>1 else ""} : {winner_string} with {highest_score} correct answer{"s" if highest_score>1 else ""}'
            await ctx.message.channel.send(msg)
        else:
            await ctx.message.channel.send('No-one got any correct answers, disgraceful...')

        self.reset()

    def reset(self):
        self.active = False
        self.participants.clear()
        self.score_map.clear()
        self.answer_map.clear()

    def all_voted(self) -> bool:
        return len(self.participants) == len(self.answer_map.keys())

    @quiz.command(name='end', aliases=['stop'])
    async def end(self, ctx):
        print("End called!")
        if not self.active:
            await ctx.mesage.channel.send('No Active Quiz!')
        else:
            await ctx.message.channel.send('Ending Quiz...')
            self.active = False








