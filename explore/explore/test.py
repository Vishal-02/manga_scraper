import sqlite3
from selenium import webdriver



con = sqlite3.connect("comick.db")
cur = con.cursor()



# con.commit()
cur.close()
con.close()