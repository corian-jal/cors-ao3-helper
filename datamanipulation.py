### DATA MANIPULATION
# create a pandas dataframe and allow for sorting + filtering
import numpy as np
import pandas as pd
from datetime import datetime
import AO3

def createArchive(library : list) -> pd.DataFrame:
    return pd.DataFrame(library, columns=['work_id', 'link', 'title', 'author', 'rating', 'warnings', 'fandoms', 'ships', 'characters', 'freeforms', 'word_count', 'chapter_count', 'series', 'kudos', 'hits', 'last_update', 'last_visit', 'visit_num'])

def loadArchive(filename : str) -> pd.DataFrame:
    return pd.read_csv(filename)

def printColumns(archive : pd.DataFrame) -> None:
    print(list(archive.columns))

def countRows(archive :pd.DataFrame) -> int:
    return archive.shape[0]

def printArchive(archive : pd.DataFrame, cols : list, rows : int) -> None:
    if rows > countRows(archive):
        rows = countRows(archive)
    elif rows < 0:
        rows = 0
    print(archive.loc[:, cols].head(rows))

def sortBy(archive : pd.DataFrame, col : str, asc : bool) -> pd.DataFrame:
    return archive.sort_values(by=col, ascending=asc)

# filter functions, essentially "does x appear in y column"

def storeArchive(archive : pd.DataFrame, filename : str) -> None:
    archive.to_csv(filename)