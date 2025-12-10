### DATA MANIPULATION
# create a pandas dataframe and allow for sorting + filtering
import numpy as np
import pandas as pd
import AO3

def createArchive(library : list, filename : str):
    archive = pd.DataFrame(library, columns=['work_id', 'link', 'title', 'author', 'rating', 'warnings', 'fandoms', 'ships', 'characters', 'freeforms', 'word_count', 'chapter_count', 'series', 'kudos', 'hits', 'last_update', 'visit_history'])
    archive.to_csv(filename)