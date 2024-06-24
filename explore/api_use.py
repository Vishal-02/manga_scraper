import requests
from pprint import pprint
import sqlite3

'''
    - have to make selective downloads available
    - might need tkinter for everything i have planned
'''

# returns the title, current and latest from "all" the databases
def all_db_data():
    data = []

    con = sqlite3.connect("comick.db")
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM Manga"):
        title, url, current, latest, hid = row
        data.append([title, current, latest])

    cur.close()
    con.close()

    con = sqlite3.connect("mangakakalot.db")
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM Manga"):
        title, url, current, latest = row

        current = current.split(":")[0].split(" ")[-1]
        if current == "" or current == " ":
            current = 0
        elif "." in current:
            current = float(current)
        else:
            current = int(current)

        latest = latest.split(":")[0].split(" ")[-1]
        if latest == "" or latest == " ":
            latest = 0
        elif "." in latest:
            latest = float(latest)
        else:
            latest = int(latest)

        data.append([title, current, latest])

    cur.close()
    con.close()

    return data

# returns the data from the database, that's all it does
def db_data():
    con = sqlite3.connect("comick.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM Manga")
    result = cur.fetchall()

    cur.close()
    con.close()
    
    return result

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


if __name__ == '__main__':
    pass
    # # this has to be a list of lists, goes into the insert_values function
    # data = [
        
    # ]

    # insert_values(data)