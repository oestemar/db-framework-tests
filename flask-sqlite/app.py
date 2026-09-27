import csv
import sqlite3
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

DB_NAME = "address.db"

# ============================
# DB接続
# ============================
def get_db():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn

# ============================
# 一覧表示
# ============================
@app.route("/")
def display():

    conn = get_db()
    cur = conn.cursor()

    keyword = request.args.get("keyword", "").strip()
    birthday_from = request.args.get("birthday_from", "")
    birthday_to = request.args.get("birthday_to", "")
    keywords = keyword.split()

    birthday_from = (
        birthday_from
        .replace("/", "-")
    )

    birthday_to = (
        birthday_to
        .replace("/", "-")
    )

    print("birthday_from =", birthday_from)
    print("birthday_to =", birthday_to)

    sql = """
        SELECT *
        FROM addresses
        WHERE 1 = 1
    """

    params = []


    for word in keywords:
        sql += """
            AND
            (
                name LIKE ?
                OR address LIKE ?
            )
        """

        params.append(f"%{word}%")
        params.append(f"%{word}%")

    if birthday_from:

        sql += """
            AND birthday >= ?
        """

        params.append(birthday_from)

    if birthday_to:

        sql += """
            AND birthday <= ?
        """

        params.append(birthday_to)

    sql += """
        ORDER BY id ASC
    """
    print(sql)
    print(params)

    cur.execute(sql, params)

    records = cur.fetchall()

    conn.close()

    return render_template(
        "display.html",
        records=records
    )

# ============================
# 詳細表示
# ============================
@app.route("/detail/<int:id>")
def detail(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM addresses
        WHERE id = ?
    """, (id,))

    record = cur.fetchone()

    conn.close()

    return render_template(
        "detail.html",
        record=record
    )

# ============================
# 登録 GET
# ============================
@app.route("/register", methods=["GET"])
def register():

    return render_template("register.html")

# ============================
# 登録 POST
# ============================
@app.route("/register", methods=["POST"])
def register_post():

    conn = get_db()
    cur = conn.cursor()
    
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
        ?,?,?,?,?,?,?,?,?,?,?,?
        )
        """, (
        request.form["name"],
        request.form["kana"],
        request.form["age"],
        request.form["birthday"],
        request.form["gender"],
        request.form["blood_type"],
        request.form["email"],
        request.form["tel"],
        request.form["mobile"],
        request.form["postal_code"],
        request.form["address"],
        request.form["company"]
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("display"))

# ============================
# CSV登録 GET
# ============================
@app.route("/register-csv", methods=["GET"])
def register_csv():

    return render_template("register_csv.html")

# ============================
# CSV登録 POST
# ============================
@app.route("/register-csv", methods=["POST"])
def register_csv_post():

    file = request.files["csvfile"]

    conn = get_db()
    cur = conn.cursor()

    reader = csv.DictReader(
        file.stream.read().decode("utf-8-sig").splitlines()
    )

    for row in reader:
        birthday = row["birthday"]
        birthday = (
            birthday
            .replace("年", "-")
            .replace("月", "-")
            .replace("日", "")
        )

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
            ?,?,?,?,?,?,?,?,?,?,?,?
            )""",(
                row["name"],
                row["kana"],
                row["age"],
                birthday,
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

    return redirect(url_for("display"))

# ============================
# 編集画面 GET
# ============================
@app.route("/edit/<int:id>", methods=["GET"])
def edit_get(id):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT *
    FROM addresses
    WHERE id = ?
    """, (id,))
    
    record = cur.fetchone()
    
    conn.close()
    
    return render_template(
    "edit.html",
    record=record
    )

# ============================
# 編集処理 POST
# ============================
@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE addresses
        SET
        name = ?,
        kana = ?,
        age = ?,
        birthday = ?,
        gender = ?,
        blood_type = ?,
        email = ?,
        tel = ?,
        mobile = ?,
        postal_code = ?,
        address = ?,
        company = ?,
        updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
        
        request.form["name"],
        request.form["kana"],
        request.form["age"],
        request.form["birthday"],
        request.form["gender"],
        request.form["blood_type"],
        request.form["email"],
        request.form["tel"],
        request.form["mobile"],
        request.form["postal_code"],
        request.form["address"],
        request.form["company"],
    id
    
    ))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for("display"))

# ============================
# 削除確認 GET
# ============================
@app.route("/delete/<int:id>", methods=["GET"])
def delete_get(id):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT *
    FROM addresses
    WHERE id = ?
    """, (id,))
    
    address = cur.fetchone()
    
    conn.close()
    
    return render_template(
    "delete.html",
    address=address
    )

# ============================
# 削除処理 POST
# ============================
@app.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    DELETE
    FROM addresses
    WHERE id = ?
    """, (id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for("display"))