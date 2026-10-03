# create_db.py
import psycopg2

DB_NAME = "fastapi_postgres_native_db"

conn = psycopg2.connect(
	host="localhost",
	dbname="fastapi_postgres_native_db",
	user="postgres",
	password="postgres"
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