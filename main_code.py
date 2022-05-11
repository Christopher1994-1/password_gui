import sqlite3

db = sqlite3.connect("passwords.db")
conn = db.cursor()

# conn.execute("CREATE TABLE passwords (account, user_info, password)")
# db.commit()