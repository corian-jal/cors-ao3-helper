### DATA MANIPULATION
# create a pandas dataframe and allow for sorting + filtering
import numpy as np
import pandas as pd
from datetime import datetime
from ast import literal_eval
import AO3

def createArchive(library : list) -> pd.DataFrame:
    return pd.DataFrame(library, columns=['work_id', 'link', 'title', 'author', 'rating', 'warnings', 'fandoms', 'ships', 'characters', 'freeforms', 'word_count', 'chapter_count', 'series', 'kudos', 'hits', 'last_update', 'last_visit', 'visit_num', 'last_known_page', 'html'])

def loadArchive(filename : str) -> pd.DataFrame:
    # turn str(list[str]) back into list[str] in here?
    try:
        archive = pd.read_csv(filename)
    except: 
        archive = None
    return archive

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

    if col in ['warnings', 'fandoms', 'ships', 'characters', 'freeforms', 'series']: #add author when mult is supported
        # each entry is a str representation of a list of strings >> only if loaded, not when just built
        tags_str = all_tags
        all_tags = []
        for tag_list in tags_str:
            all_tags = all_tags + (literal_eval(tag_list))

    halloffame = {}
    for tag in all_tags:
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

def getAllHTML(archive : pd.DataFrame) -> str:
    allhtml = archive['html']
    page = ''
    for entry in allhtml:
        page = page + '\n' + entry
    return page

def storeArchive(archive : pd.DataFrame, filename : str) -> None:
    archive.to_csv(filename)