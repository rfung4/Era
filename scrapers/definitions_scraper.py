from scrapers.util import make_soup

voc = 'https://www.vocabulary.com/lists/52473'

def get_word_dict():
    soup = make_soup()
    word_tags = soup.findAll(class_='entry learnable')
    words = {}

    for tag in word_tags:
        word = tag.find(class_='word dynamictext').text
        definition = tag.find(class_='definition').text
        words[word] = definition

    return words

wo = get_word_dict()

word_file = open("definitions.txt", "a")
for key, value in wo.items():
    word_file.write(f'{key}={value}\n')

word_file.close()















