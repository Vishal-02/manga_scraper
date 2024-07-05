import requests
from dotenv import load_dotenv
from os import getenv
import sqlite3

'''
    - have to make selective downloads available
'''
load_dotenv()
DB_PATH = getenv('DB_PATH')

# returns the data from the database, that's all it does
def db_data():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT * FROM Manga")
    result = cur.fetchall()

    for i, row in enumerate(result):
        result[i] = (row[0], row[2], row[3])

    cur.close()
    con.close()
    
    return result

# gets the entire response for a specific manga name in comick
def get_response(name, page=1, limit=1):
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
        if len(response.json()) > 0:
            return response.json()[0]
        else:
            return "No Result"
    else:
        print(response.status_code)
        print(response.text)
        print("Error")
        return False

# gets the hid for a specific manga name in comick
def get_hid(title):
    result = get_response(title)
    if result == "No Result":
        return result
    return result['hid']

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
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM Manga"):
        title, url, current, latest, hid, source, desc = row
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
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for i, row in enumerate(data):
        title, url, current, latest, hid, source = row
        if hid == None:
            hid = get_hid(title)
        if latest == None:
            latest = get_latest_chapter(hid)
        data[i] = (title, url, current, latest, hid, source)

    cur.executemany("INSERT INTO Manga VALUES(?, ?, ?, ?, ?, ?)", data)
    for row in cur.execute("SELECT * FROM Manga"):
        print(row)

    con.commit()
    cur.close()
    con.close()

# gets the chapter image
def get_image(hid):
    base_url = f"https://api.comick.fun/chapter/{hid}/get_images"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url=base_url, headers=headers)
    return response


if __name__ == '__main__':
    hid = 'oBfcDAEn'
    image = get_image(hid)
    print(image)
    # con = sqlite3.connect(DB_PATH)
    # cur = con.cursor()

    # for row in cur.execute("SELECT * FROM Manga"):
    #     pprint(row)

    # cur.close()
    # con.close()
    


'''
Function Graveyard:

this function helped me take stuff from my mangakakalot database and put them in my comick database
since all the manga i got for kakalot were there in comick, and comick has an api i can use
that, and i can't scrape from kakalot

def search_for_titles():
    con = sqlite3.connect("mangakakalot.db")
    cur = con.cursor()
    comick_con = sqlite3.connect("comick.db")
    comick_cur = comick_con.cursor()

    data = cur.execute("SELECT * FROM Manga").fetchall()
    for row in data:
        title, url, current, latest = row
        manga_response = get_response(title)
        desc, hid = manga_response['desc'], manga_response['hid']
        current, latest = fix_chapters(current, latest)

        comick_cur.execute("SELECT * FROM Manga WHERE title=?", (title,))
        present = comick_cur.fetchall()
        if len(present) == 0 and hid != "No Result":
            comick_cur.execute("INSERT INTO Manga VALUES(?, ?, ?, ?, ?, ?, ?)", (title, '', current, latest, hid, 'comick', desc))
    
    # comick_con.commit()
    comick_cur.close()
    comick_con.close()
    cur.close()
    con.close()

    
i used this to get the proper chapter numbers from the mangakakalot database
it was 'chapter 1', 'chapter 52' and so on in the kakalot db, i wanted just the numbers

def fix_chapters(current, latest):
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
    
    return current, latest
'''