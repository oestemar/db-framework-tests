# create_db.py
import sqlite3

DB_NAME = "address.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS addresses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
kana TEXT NOT NULL,
age INTEGER,
birthday TEXT,
gender TEXT,
blood_type TEXT,
email TEXT,
tel TEXT,
mobile TEXT,
postal_code TEXT,
address TEXT,
company TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP 
    DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
print("DB作成完了")