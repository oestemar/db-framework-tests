# create_db.py
import psycopg2
import os
import dotenv
dotenv.load_dotenv()

print(os.getenv("POSTGRESHOST"))
print(os.getenv("POSTGRESPORT"))
print(os.getenv("POSTGRESUSER"))
print(os.getenv("POSTGRESPASSWORD"))
print(os.getenv("POSTGRESDATABASE"))

conn = psycopg2.connect(
        host = os.getenv('POSTGRESHOST'),
        user = os.getenv('POSTGRESUSER'),
        password = os.getenv('POSTGRESPASSWORD'),
        port = int(os.getenv('POSTGRESPORT')),
        database = os.getenv('POSTGRESDATABASE'),
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