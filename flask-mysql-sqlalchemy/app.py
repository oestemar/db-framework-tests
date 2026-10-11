import csv
from flask import Flask,render_template,request,redirect,url_for
from models import Address, db
from sqlalchemy import or_
from datetime import datetime
import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
import os

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://"
    f"{os.getenv('MYSQLUSER')}:"
    f"{os.getenv('MYSQLPASSWORD')}@"
    f"{os.getenv('MYSQLHOST')}:"
    f"{os.getenv('MYSQLPORT')}/"
    f"{os.getenv('MYSQLDATABASE')}"
)

db.init_app(app)

# ============================
# 一覧表示
# ============================
@app.route("/")
def display():

    keyword = request.args.get("keyword", "").strip()
    birthday_from = request.args.get("birthday_from", "")
    birthday_to = request.args.get("birthday_to", "")
    keywords = keyword.split()

    query = Address.query

    birthday_from = (
        birthday_from
        .replace("/", "-")
    )

    birthday_to = (
        birthday_to
        .replace("/", "-")
    )

    for word in keywords:
        query = query.filter(
            or_(
                Address.name.like(f"%{word}%"),
                Address.address.like(f"%{word}%")
            )
        )

    if birthday_from:
        query = query.filter(
            Address.birthday >= birthday_from
        )

    if birthday_to:
        query = query.filter(
            Address.birthday <= birthday_to
        )

    records = query.order_by(
        Address.id.asc()
    ).all()

    return render_template(
        "display.html",
        records=records
    )

# ============================
# 詳細表示
# ============================
@app.route("/detail/<int:id>")
def detail(id):

    record = Address.query.get_or_404(id)

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

    birthday = request.form["birthday"]
    birthday = (
        birthday
        .replace("/", "-")
    )

    birthday = datetime.strptime(
        birthday,
        "%Y-%m-%d"
    ).date()
    
    record = Address (
        name = request.form["name"],
        kana = request.form["kana"],
        age = request.form["age"],
        birthday = birthday,
        gender = request.form["gender"],
        blood_type = request.form["blood_type"],
        email = request.form["email"],
        tel = request.form["tel"],
        mobile = request.form["mobile"],
        postal_code = request.form["postal_code"],
        address = request.form["address"],
        company = request.form["company"]
    )

    db.session.add(record)
    db.session.commit()

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

        birthday = datetime.strptime(
            birthday,
            "%Y-%m-%d"
        ).date()

        record = Address(
            name = row["name"],
            kana = row["kana"],
            age = row["age"],
            birthday = birthday,
            gender = row["gender"],
            blood_type = row["blood_type"],
            email = row["email"],
            tel = row["tel"],
            mobile = row["mobile"],
            postal_code = row["postal_code"],
            address = row["address"],
            company = row["company"]
        )

        db.session.add(record)
    db.session.commit()

    return redirect(url_for("display"))

# ============================
# 編集画面 GET
# ============================
@app.route("/edit/<int:id>", methods=["GET"])
def edit_get(id):

    record = Address.query.get_or_404(id)

    return render_template(
        "edit.html",
        record=record
    )

# ============================
# 編集処理 POST
# ============================
@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    
    birthday = request.form["birthday"]

    birthday = datetime.strptime(
        birthday,
        "%Y-%m-%d"
    ).date()

    record = Address.query.get_or_404(id)

    record.name = request.form["name"]
    record.kana = request.form["kana"]
    record.age = request.form["age"]
    record.birthday = birthday
    record.gender = request.form["gender"]
    record.blood_type = request.form["blood_type"]
    record.email = request.form["email"]
    record.tel = request.form["tel"]
    record.mobile = request.form["mobile"]
    record.postal_code = request.form["postal_code"]
    record.address = request.form["address"]
    record.company = request.form["company"]

    db.session.commit()
    
    return redirect(url_for("display"))

# ============================
# 削除確認 GET
# ============================
@app.route("/delete/<int:id>", methods=["GET"])
def delete_get(id):

    record = Address.query.get_or_404(id)

    return render_template(
    "delete.html",
    record=record
    )

# ============================
# 削除処理 POST
# ============================
@app.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):

    record = Address.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    return redirect(url_for("display"))

with app.app_context():
    db.create_all()