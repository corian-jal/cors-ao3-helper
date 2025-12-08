# imports
import requests
from bs4 import BeautifulSoup
import AO3

# define fic class
class Fic:
    def __init__(self, id, link, title, authors, rating, warnings, fandoms, 
                 ships, characters, freeforms, word_count, chapter_count, 
                 last_update, last_visit) -> None:
        self.work_id = id
        self.link = link
        self.title = title
        self.authors = authors
        self.rating = rating
        self.warnings = warnings
        self.fandoms = fandoms
        self.ships = ships
        self.characters = characters
        self.freeforms = freeforms
        self.word_count = word_count
        self.chapter_count = chapter_count
        self.last_update = last_update
        self.last_visit = last_visit

    def __repr__(self):
        return f"Fic#{self.work_id} {self.link}\n {self.title} by {self.authors}\n {self.rating} / {self.warnings}\n {self.fandoms}\n {self.ships}\n {self.characters}\n {self.freeforms}\n {self.word_count} -- {self.chapter_count}\n {self.last_update} / {self.last_visit}\n"

# procure html; for now, use a sample html
with open('mfl-page1sample.html', encoding='utf-8') as file:
    sample = file.read()

# beautifulsoup parsing
soup = BeautifulSoup(sample, 'html.parser')
ordlist = soup.find('ol', 'reading work index group') # get the whole ordered list of fics
litem = ordlist.find('li') # get the first list item
#print(litem.prettify())

# parse first list item into a fic object
id = ''.join(filter(str.isnumeric, litem['id']))
link = 'https://archiveofourown.org/works/' + id

tcard = litem.find('h4').text.split('by')
title = tcard[0].strip()
author = tcard[1].strip() # what is anon? what if >1?

req_tags = litem.find('ul', 'required-tags').text.splitlines()
rating = req_tags[1].strip()
warnings = req_tags[2].strip() # account for plural. and what about the other two boxes?
# could get warnings from tags later too; might be easier

fandoms = []
for fandom in litem.find('h5', 'fandoms heading').find_all('a'):
    fandoms.append(fandom.text)

# what if there are no ships/characters/freeforms?
ships = []
for ship in litem.find_all('li', 'relationships'):
    ships.append(ship.text)

charas = []
for char in litem.find_all('li', 'characters'):
    charas.append(char.text)

freeforms = []
for tag in litem.find_all('li', 'freeforms'):
    freeforms.append(tag.text)

word_count = litem.find('dd', 'words').text
chapter_count = litem.find('dd', 'chapters').text
last_update = litem.find('p', 'datetime').text #make some kind of real date object?
marked_blurb = litem.find('h4', 'viewed heading').text.splitlines()
visit_history = [marked_blurb[1], marked_blurb[5].strip()]

fic1 = Fic(id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, last_update, visit_history)
print(fic1)