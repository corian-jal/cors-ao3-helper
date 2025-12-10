### PARSING HTML TO FIC OBJECT
# given html(s), extract relevant fic information
from bs4 import BeautifulSoup

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


def mflPageToFicList(sample : str) -> list:
    # beautifulsoup parsing
    soup = BeautifulSoup(sample, 'html.parser')

    # on mfl page, fics are list items (li) in an ordered list (ol)
    ficsonpage = soup.find('ol', 'reading work index group').find_all('li', role='article')
    # need to account for deleted + mystery fics, right?
    print(len(ficsonpage), ' fics found\n-----------------')

    library_real = [] # objects
    library = [] # lists for pds

    # parse each fic on the page into a fic object
    # ...for what? keep a local list of them all? -> is the object needed for anything or is it redundant?
    for fic in ficsonpage:
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

        ships = []
        for ship in fic.find_all('li', class_='relationships'):
            ships.append(ship.text)

        charas = []
        for char in fic.find_all('li', class_='characters'):
            charas.append(char.text)

        freeforms = []
        for tag in fic.find_all('li', class_='freeforms'):
            freeforms.append(tag.text)

        word_count = int(fic.find('dd', class_='words').text.replace(',',''))
        chapter_count = fic.find('dd', class_='chapters').text
        
        series = 'None'
        series_maybe = fic.find('ul', class_='series')
        if series_maybe != None:
            series = series_maybe.text.strip()

        kudos = int(fic.find('dd', class_='kudos').text.replace(',',''))
        hits = int(fic.find('dd', class_='hits').text.replace(',',''))
        last_update = fic.find('p', class_='datetime').text #make some kind of real date object?
        marked_blurb = fic.find('h4', class_='viewed heading').text.splitlines()
        last_visit = marked_blurb[1] #make some kind of real date object?
        visit_num = marked_blurb[5].strip()

        logged_fic = Fic(id, link, title, author, rating, warnings, fandoms, ships, charas, freeforms, word_count, chapter_count, series, kudos, hits, last_update, last_visit, visit_num)
        library_real.append(logged_fic)
        library.append(logged_fic.ficToList())
        #print(logged_fic)
        #print('----------------------------------------------------------------')
        #input("Press Enter to continue...")
    return library