import sqlite3

con = sqlite3.connect("comick.db")
cur = con.cursor()



cur.close()
con.close()