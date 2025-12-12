### DIRECT INTERACTIONS WITH AO3
# properly access the relevant html page and return the relevant html(s)
import os
import requests
from bs4 import BeautifulSoup
import time

# placeholder -- using a single local html file for now; interacting with AO3 to be configured later
# get and return all html for all pages or one at a time? probably all at once to avoid contamination
def getMFLSample () -> str:
    with open('./files/mfl-page1sample.html', encoding='utf-8') as file:
        sample = file.read()
    return sample

# referenced wendytg's ao3 api code to figure out that a auth token was needed + what logging in with it looks like
# https://github.com/wendytg/ao3_api/blob/master/AO3/session.py
def getMFL () -> list:
    
    with requests.Session() as s:
        user = input("What is your AO3 username?\n> ")
        passw = input("And your password? Promise I'll keep it a secret.\n> ")
        os.system('cls')
        print("Logging you in...")

        soup = BeautifulSoup(s.get('https://archiveofourown.org/users/login').text, 'html.parser')
        token = soup.find("input", {"name": 'authenticity_token'})["value"]
        payload = {
            'user[login]': user,
            'user[password]': passw,
            'authenticity_token': token
        }

        mfl = []

        login = s.post("https://archiveofourown.org/users/login", params=payload, allow_redirects=False)
        if login.status_code == 302:
            print("Grabbing your Marked for Later works now...")
            page_num = 1

            while True:
                link = 'https://archiveofourown.org/users/' + user + '/readings?show=to-read&page=' + str(page_num)
                mfl_pg = s.get(link)
                
                soup = BeautifulSoup(mfl_pg.text, 'html.parser')                
                if soup.find('ol', 'reading work index group') is None:
                    if page_num == 1:
                        input("Either you have no works Marked for Later or log in failed. Please check and try again.\n> ")
                    break
                
                mfl.append(mfl_pg.text)
                page_num += 1
                print("Sleeping for 3s before loading page " + str(page_num) + ".")
                time.sleep(3) # some suggest randomizing this between 1-3
        else:
            print("Sorry, I got a page error.")

        return mfl