### DATA MANIPULATION
# create a pandas dataframe and allow for sorting + filtering
import numpy as np
import pandas as pd
import AO3

def createArchive(library : list) -> pd.DataFrame:
    return pd.DataFrame(library, columns=['work_id', 'link', 'title', 'author', 'rating', 'warnings', 'fandoms', 'ships', 'characters', 'freeforms', 'word_count', 'chapter_count', 'series', 'kudos', 'hits', 'last_update', 'last_visit', 'visit_num'])

def loadArchive(filename : str) -> pd.DataFrame:
    return pd.read_csv(filename)

def printArchive(archive : pd.DataFrame, cols : list ) -> None:
    # list of names of the wanted columns
    print(archive.loc[:, cols])

# currently works for non-dates, so word, kudo, hit, visit# and ig strings if you want alphabetical
# add functionality for dates
def sortBy(archive : pd.DataFrame, col : str, asc : bool) -> pd.DataFrame:
    return archive.sort_values(by=col, ascending=asc)

# filter functions, essentially "does x appear in y column"

def storeArchive(archive : pd.DataFrame, filename : str) -> None:
    archive.to_csv(filename)