### DIRECT INTERACTIONS WITH AO3
# properly access the relevant html page and return the relevant html(s)
import requests

# placeholder -- using a local html file for now; interacting with AO3 to be configured later
# get and return all html for all pages or one at a time? probably all at once to avoid contamination
def getMFLSample () -> str:
    with open('files/mfl-page1sample.html', encoding='utf-8') as file:
        sample = file.read()
    return sample