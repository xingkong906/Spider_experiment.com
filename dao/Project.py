import sqlite3

con = sqlite3.connect("../data/experiment.db")
cursor = con.cursor()
cursor.execute("created")