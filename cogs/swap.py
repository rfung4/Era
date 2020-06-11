import re
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib import parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from definitions import CHROME_DRIVER_PATH, ROOT_DIR
from scrapers.util import sleep_until

# TODO: Fix for https://www.reddit.com/r/holdmyfeedingtube/comments/ex5c7v/hmft_after_i_hit_a_cow_at_30mph/ (Upload mp4 file instead of link..)
# TODO: Regex match for valid reddit link


class swap(commands.Cog):

    reddit_link_regex = re.compile('')  # TODO!
    veddit_url = 'https://viddit.red/?url='

    def __init__(self, bot):
        self.bot = bot
        self.driver = None

    @staticmethod
    def create_web_driver() -> WebDriver:   # TODO: Move this to the bot, and add some form of queue for driver requests
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver

    def has_video_frame(self):
        return len(self.driver.find_elements_by_css_selector('video'))

    async def get_mp4_from_veddit(self, raw_url):
        request_url = parse.quote_plus(raw_url)
        full_url = self.veddit_url + request_url
        self.driver.get(full_url)
        self.driver.refresh()
        await sleep_until(10, self.has_video_frame)
        soup = BeautifulSoup(self.driver.page_source, features='lxml')
        return soup.find('video').find('source')['src']

    @commands.command(aliases=['convert', 'archive'])
    async def swap(self, ctx):
        msg = ctx.message.content.strip()
        split_msg = msg.split()

        if len(split_msg) == 1:
            await ctx.message.channel.send('Invalid format for swap command')
            return

        msg_url = split_msg[1]

        # TODO: Regex check here!

        if not self.driver:
            self.driver = self.create_web_driver()

        mp4_link = await self.get_mp4_from_veddit(msg_url)
        msg_to_send = f'{mp4_link} ({ctx.message.author.display_name})'

        await ctx.message.delete()
        await ctx.message.channel.send(msg_to_send)

        #self.driver.quit()

        # TODO: Delete original message!
        # TODO: Optimize performance by checking if video element exists (len() of findall)

