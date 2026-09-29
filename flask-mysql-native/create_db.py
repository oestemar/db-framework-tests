# create_db.py
import pymysql

DB_NAME = "address_db"
conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "Oestemarmysql",
        database = DB_NAME,
        charset = "utf8mb4",
        cursorclass = pymysql.cursors.DictCursor
    )
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS addresses(
id INT AUTO_INCREMENT PRIMARY KEY,
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
    ON UPDATE CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
print("DB作成完了")