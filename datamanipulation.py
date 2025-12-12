### DATA MANIPULATION
# create a pandas dataframe and allow for sorting + filtering
import numpy as np
import pandas as pd
from datetime import datetime
from ast import literal_eval
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

def topTags(archive : pd.DataFrame, col : str) -> pd.DataFrame:
    all_tags = archive[col].to_list()
    halloffame = {}

    for tags_str in all_tags:
        tags = literal_eval(tags_str)
        for tag in tags:
            if tag in halloffame:
                halloffame[tag] += 1
            else:
                halloffame[tag] = 1
    
    hallofframe = pd.DataFrame(list(halloffame.items()), columns=['tag', 'count'])
    return hallofframe.sort_values(by='count', ascending=False)

def filterItem(archive : pd.DataFrame, col : str, val, include : bool) -> pd.DataFrame:
    # works for full and partial
    if include:
        return archive[archive[col].str.contains(val)]
    else:
        return archive[~(archive[col].str.contains(val))]

def filterRange(archive : pd.DataFrame, col : str, start : int, end : int) -> pd.DataFrame:
    # inclusive
    return archive[(archive[col] >= start) & (archive[col] <= end)]

# or-filtering is a wishlist item

def sortBy(archive : pd.DataFrame, col : str, asc : bool) -> pd.DataFrame:
    return archive.sort_values(by=col, ascending=asc)

def storeArchive(archive : pd.DataFrame, filename : str) -> None:
    archive.to_csv(filename)