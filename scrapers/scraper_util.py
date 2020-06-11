import datetime
import urllib
from asyncio import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup


def make_soup(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    html = urlopen(req)
    soup = BeautifulSoup(html, features="lxml")
    return soup


async def sleep_until(duration: int, predicate_function):
    end = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    while datetime.datetime.now() < end:
        await sleep(0.25)
        if predicate_function():
            break
    return
