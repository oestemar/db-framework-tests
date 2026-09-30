# create_db.py
import psycopg2

DB_NAME = "address_db"
conn = psycopg2.connect(
        host = "localhost",
        user = "postgres",
        password = "postgres",
        database = DB_NAME,
    )
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS addresses(
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
kana VARCHAR(100) NOT NULL,
age INTEGER,
birthday DATE,
gender VARCHAR(20),
blood_type VARCHAR(20),
email VARCHAR(100),
tel VARCHAR(30),
mobile VARCHAR(30),
postal_code VARCHAR(20),
address VARCHAR(200),
company VARCHAR(100),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
print("DB作成完了")