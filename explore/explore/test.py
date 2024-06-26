import sqlite3
from selenium import webdriver



con = sqlite3.connect("mangakakalot.db")
cur = con.cursor()
# cur.execute("alter table Manga add description")
print(cur.execute("pragma table_info(Manga)").fetchall())

# con.commit()
cur.close()
con.close()