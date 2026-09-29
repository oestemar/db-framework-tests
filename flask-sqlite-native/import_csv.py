import sqlite3
import csv

conn = sqlite3.connect("address.db")
cur = conn.cursor()

with open(
"addresses.csv",
"r",
encoding="utf-8-sig"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        cur.execute("""
            INSERT INTO addresses(
            name,
            kana,
            age,
            birthday,
            gender,
            blood_type,
            email,
            tel,
            mobile,
            postal_code,
            address,
            company
            )
            VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
            row["name"],
            row["kana"],
            row["age"],
            row["birthday"],
            row["gender"],
            row["blood_type"],
            row["email"],
            row["tel"],
            row["mobile"],
            row["postal_code"],
            row["address"],
            row["company"]
        ))

conn.commit()
conn.close()

print("CSV取込完了")