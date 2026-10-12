# create_db.py
import psycopg2
import os

conn = psycopg2.connect(
	host=os.getenv("PGHOST"),
	user=os.getenv("PGUSER"),
	password=os.getenv("PGPASSWORD"),
	port=os.getenv("PGPORT"),
	dbname=os.getenv("POSTGRES_DB"),
)

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS addresses(
id SERIAL PRIMARY KEY,
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