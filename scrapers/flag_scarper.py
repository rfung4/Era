from urllib.request import urlopen
from definitions import FLAGS_DIR
from scrapers.scraper_util import make_soup

url = 'https://www.worldometers.info/geography/flags-of-the-world/'
base = 'https://www.worldometers.info'
flags_directory = ""


def get_flags() -> {}:
    flag_tags = make_soup(url).findAll(class_='col-md-4')

    for tag in flag_tags:
        img = urlopen(base + tag.a['href'])
        output = open(FLAGS_DIR + tag.text.replace(' ', '_') + ".gif", "wb")
        output.write(img.read())
        output.close()


if __name__ == '__main__':
    get_flags()

















