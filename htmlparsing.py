### PARSING HTML TO FIC OBJECT
# given html(s), extract relevant fic information
from bs4 import BeautifulSoup
import json
from datetime import datetime

syn_source = './files/synonyms.json'
synonyms = {}

# define fic class
class Fic:
    def __init__(self, id, link, title, authors, rating, warnings, fandoms, 
                 ships, characters, freeforms, word_count, chapter_count, 
                 series, kudos, hits, last_update, last_visit, visit_num) -> None:
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
        self.last_visit = last_visit
        self.visit_num = visit_num

    def __repr__(self):
        return f"Fic#{self.work_id} {self.link}\n {self.title} by {self.authors}\n {self.rating} / {self.warnings}\n {self.fandoms}\n {self.ships}\n {self.characters}\n {self.freeforms}\n {self.word_count} -- {self.chapter_count}\n {self.series}\n {self.kudos} kudos / {self.hits} hits\n {self.last_update} / {self.last_visit} {self.visit_num}\n"
    
    def ficToList(self) -> list: # add a reverse?
        return [self.work_id, self.link, self.title, self.authors, self.rating, self.warnings, self.fandoms, self.ships, self.characters, self.freeforms, self.word_count, self.chapter_count, self.series, self.kudos, self.hits, self.last_update, self.last_visit, self.visit_num]

with open(syn_source) as f:
    synonyms = json.load(f)

def normalizeTags(tags : list) -> list:
    new_tags = []
    for tag in tags:
        tag = tag.replace('(Anime)', '(Anime & Manga)').replace('(Manga)', '(Anime & Manga)')
        if tag in synonyms:
            tag = synonyms.get(tag)
        new_tags.append(tag)
    return list(dict.fromkeys(new_tags)) #remove dups and maintain order?

def mflPageToFicList(sample : str, page_num : int) -> list:
    # beautifulsoup parsing
    soup = BeautifulSoup(sample, 'html.parser')

    # on mfl page, fics are list items (li) in an ordered list (ol)
    ficsonpage = soup.find('ol', 'reading work index group').find_all('li', role='article')

    #library_real = [] # objects
    library = [] # lists for pds

    # parse each fic on the page into a fic object
    # ...for what? keep a local list of them all? -> is the object needed for anything or is it redundant?
    for fic in ficsonpage:
        try: 
            #print(fic.prettify())

            id = ''.join(filter(str.isnumeric, fic['id']))
            link = 'https://archiveofourown.org/works/' + id

            tcard = fic.find('h4', class_='heading').find_all('a')
            title = tcard[0].text
            author = 'Anonymous'
            if len(tcard) > 1:
                author = tcard[1].text
                # >1 author? maybe can just make this a loop
                # what if orphaned?

            # it is always required and always first in required tags
            rating = fic.find('ul', class_='required-tags').find('li').text

            warnings = []
            for warning in fic.find_all('li', class_='warnings'):
                warnings.append(warning.text)

            fandoms = []
            for fandom in fic.find('h5', class_='fandoms heading').find_all('a'):
                fandoms.append(fandom.text)
            fandoms = normalizeTags(fandoms)

            ships = []
            for ship in fic.find_all('li', class_='relationships'):
                ships.append(ship.text)
            ships = normalizeTags(ships)

            charas = []
            for char in fic.find_all('li', class_='characters'):
                charas.append(char.text)
            charas = normalizeTags(charas)

            freeforms = []
            for tag in fic.find_all('li', class_='freeforms'):
                freeforms.append(tag.text)
            freeforms = normalizeTags(freeforms)

            word_count = int(fic.find('dd', class_='words').text.replace(',',''))
            chapter_count = fic.find('dd', class_='chapters').text
            
            # might be >1 series, no series field at all if none
            series = ['Not a part of a series.']
            series_maybe = fic.find('ul', class_='series')
            if series_maybe is not None:
                series = []
                for entry in series_maybe.find_all('li'):
                    series.append(entry.text.strip())

            kudos = int(fic.find('dd', class_='kudos').text.replace(',',''))
            hits = int(fic.find('dd', class_='hits').text.replace(',',''))
            last_update = datetime.strptime(fic.find('p', class_='datetime').text, '%d %b %Y') #19 Aug 2025
            marked_blurb = list(filter(lambda x: 'isit' in x, fic.find('h4', class_='viewed heading').text.replace('once', '1').splitlines()))
            last_visit = datetime.strptime(marked_blurb[0][14:25], '%d %b %Y') #Last visited: 01 Dec 2025
            visit_num = int(''.join(filter(str.isnumeric, marked_blurb[1].strip()))) #Visited 5 times

            # if i save each html, i can output them to a file and get something readable in browser, though the links don't work. 
            # can i link that to ao3 somehow? or format it? or make at least a link to the fic work?

            #logged_fic = Fic(id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, series, kudos, hits, last_update, last_visit, visit_num)
            #library_real.append(logged_fic)
            log = [id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, series, kudos, hits, last_update, last_visit, visit_num, page_num, str(fic)]
            library.append(log)
            #print(logged_fic)
            #print('----------------------------------------------------------------')
            #input("Press Enter to continue...")
        except:
            print("Something weird happened on page " + str(page_num))
            continue
    return library