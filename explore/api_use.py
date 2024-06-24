import requests
from pprint import pprint
import sqlite3

'''
    - have to make selective downloads available
    - might need tkinter for everything i have planned
'''

# gets the hid for a specific manga name in comick
def get_hid(name, page=1, limit=1):
    base_url = "https://api.comick.fun/v1.0/search/"

    params = {
        'q': name,
        'limit': limit,
        'page': page,
        't': 'false'
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url=base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()[0]['hid']
    else:
        print(response.status_code)
        print(response.text)
        print("Error")
        return False

# gets the latest chapter for a specific hid
def get_latest_chapter(hid, limit=1, page=1, lang='en'):
    base_url = f"https://api.comick.fun/comic/{hid}/chapters"

    params = {
        'limit': limit,
        'page': page,
        'lang': lang
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url=base_url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['chapters'][0]['chap']
    else:
        print("Error")
        return False

# checks for and updates the latest chapter of the stuff in the db
def update_latest():
    con = sqlite3.connect("comick.db")
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM Manga"):
        title, url, current, latest, hid = row
        latest_chapter = int(get_latest_chapter(hid))
        updated_manga = []

        if latest_chapter > latest:
            cur.execute("UPDATE Manga set latest=? where title=?", (latest_chapter, title))
            updated_manga.append((latest_chapter, title))

    con.commit()
    cur.close()
    con.close()

    return updated_manga

# inserts new entries into the db, for more comicks i might wanna read 
# i should proabaly automate this too, would be useful to check and update my current read chapters 
def insert_values(data):
    con = sqlite3.connect("comick.db")
    cur = con.cursor()

    for i, row in enumerate(data):
        title, url, current, latest, hid = row
        if hid == None:
            hid = get_hid(title)
        if latest == None:
            latest = get_latest_chapter(hid)
        data[i] = (title, url, current, latest, hid)

    cur.executemany("INSERT INTO Manga VALUES(?, ?, ?, ?, ?)", data)
    for row in cur.execute("SELECT * FROM Manga"):
        print(row)

    con.commit()
    cur.close()
    con.close()


# # this has to be a list of lists, goes into the insert_values function
data = [
    ["The Beginning After The End", "https://comick.io/comic/00-the-beginning-after-the-end-1", 174, None, None]
]

insert_values(data)