# imports
import requests
from bs4 import BeautifulSoup
import AO3

# define fic class
class Fic:
    def __init__(self, id, link, title, authors, rating, warnings, fandoms, 
                 ships, characters, freeforms, word_count, chapter_count, 
                 kudos, hits, last_update, last_visit) -> None:
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
        # what if it's in a series?
        self.kudos = kudos
        self.hits = hits
        self.last_update = last_update
        self.last_visit = last_visit # just date or do i want to keep visit#? standardize format?

    def __repr__(self):
        return f"Fic#{self.work_id} {self.link}\n {self.title} by {self.authors}\n {self.rating} / {self.warnings}\n {self.fandoms}\n {self.ships}\n {self.characters}\n {self.freeforms}\n {self.word_count} -- {self.chapter_count}\n {self.kudos} kudos / {self.hits} hits\n {self.last_update} / {self.last_visit}\n"

### DIRECT INTERACTIONS WITH AO3
# using a local html file for now; interacting with AO3 to be configured later
with open('mfl-page1sample.html', encoding='utf-8') as file:
    sample = file.read()

### PARSING HTML TO FIC OBJECT
# beautifulsoup parsing
soup = BeautifulSoup(sample, 'html.parser')

# on mfl page, fics are list items (li) in an ordered list (ol)
ordlist = soup.find('ol', 'reading work index group') 
ficsonpage = ordlist.find_all('li')

# parse each fic on the page into a fic object
# ...for what? keep a local list of them all?
# also remember to add a format-to-csv function to class, if not innate to pandas?
for fic in ficsonpage:
    #print(fic.prettify())

    id = ''.join(filter(str.isnumeric, fic['id']))
    link = 'https://archiveofourown.org/works/' + id

    tcard = fic.find('h4').text.split('by')
    title = tcard[0].strip()
    author = tcard[1].strip() # what is anon? what if >1?

    req_tags = fic.find('ul', 'required-tags').text.splitlines()
    rating = req_tags[1].strip()
    warnings = req_tags[2].strip() # account for plural. and what about the other two boxes?
    # could get warnings from tags later too; might be easier

    fandoms = []
    for fandom in fic.find('h5', 'fandoms heading').find_all('a'):
        fandoms.append(fandom.text)

    # what if there are no ships/characters/freeforms?
    ships = []
    for ship in fic.find_all('li', 'relationships'):
        ships.append(ship.text)

    charas = []
    for char in fic.find_all('li', 'characters'):
        charas.append(char.text)

    freeforms = []
    for tag in fic.find_all('li', 'freeforms'):
        freeforms.append(tag.text)

    word_count = fic.find('dd', 'words').text
    chapter_count = fic.find('dd', 'chapters').text
    kudos = fic.find('dd', 'kudos').text
    hits = fic.find('dd', 'hits').text
    last_update = fic.find('p', 'datetime').text #make some kind of real date object?
    marked_blurb = fic.find('h4', 'viewed heading').text.splitlines()
    visit_history = [marked_blurb[1], marked_blurb[5].strip()]

    logged_fic = Fic(id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, kudos, hits, last_update, visit_history)
    print(logged_fic)
    break