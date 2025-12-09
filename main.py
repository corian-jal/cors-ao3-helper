# imports
import requests
from bs4 import BeautifulSoup
import AO3

# define fic class
class Fic:
    def __init__(self, id, link, title, authors, rating, warnings, fandoms, 
                 ships, characters, freeforms, word_count, chapter_count, 
                 series, kudos, hits, last_update, last_visit) -> None:
        self.work_id = id
        self.link = link
        # do i want to track if it's restricted?
        self.title = title
        self.authors = authors # only tracking the first for now
        # what if it's a gift?
        self.rating = rating
        self.warnings = warnings
        self.fandoms = fandoms
        self.ships = ships
        self.characters = characters
        self.freeforms = freeforms
        self.word_count = word_count
        self.chapter_count = chapter_count
        self.series = series
        self.kudos = kudos
        self.hits = hits
        self.last_update = last_update
        self.last_visit = last_visit # just date or do i want to keep visit#? standardize format?

    def __repr__(self):
        return f"Fic#{self.work_id} {self.link}\n {self.title} by {self.authors}\n {self.rating} / {self.warnings}\n {self.fandoms}\n {self.ships}\n {self.characters}\n {self.freeforms}\n {self.word_count} -- {self.chapter_count}\n {self.series}\n {self.kudos} kudos / {self.hits} hits\n {self.last_update} / {self.last_visit}\n"

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

    tcard = fic.find('h4', 'heading').find_all('a')
    title = tcard[0].text
    author = tcard[1].text # will it say anon? check if >1?

    # it is always required and always first in required tags
    rating = fic.find('ul', 'required-tags').find('li').text

    warnings = []
    for warning in fic.find_all('li', 'warnings'):
        warnings.append(warning.text)

    fandoms = []
    for fandom in fic.find('h5', 'fandoms heading').find_all('a'):
        fandoms.append(fandom.text)

    # what if there are no ships/characters/freeforms? should be fine but double-check.
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
    
    series = 'None'
    series_maybe = fic.find('ul', 'series')
    if series_maybe != None:
        series = series_maybe.text.strip()

    kudos = fic.find('dd', 'kudos').text
    hits = fic.find('dd', 'hits').text
    last_update = fic.find('p', 'datetime').text #make some kind of real date object?
    marked_blurb = fic.find('h4', 'viewed heading').text.splitlines()
    visit_history = [marked_blurb[1], marked_blurb[5].strip()]

    logged_fic = Fic(id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, series, kudos, hits, last_update, visit_history)
    print(logged_fic)
    break