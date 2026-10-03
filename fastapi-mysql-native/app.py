import csv
import pymysql
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_NAME = "fastapi_mysql_native_db"

# ============================
# DB接続
# ============================
def get_db():

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Oestemarmysql",
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    return conn

# ============================
# 一覧表示
# ============================
@app.get("/")
def display(request: Request):

    conn = get_db()
    cur = conn.cursor()

    keyword = request.query_params.get("keyword", "").strip()
    birthday_from = request.query_params.get("birthday_from", "")
    birthday_to = request.query_params.get("birthday_to", "")
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
                name LIKE %s
                OR address LIKE %s
            )
        """

        params.append(f"%{word}%")
        params.append(f"%{word}%")

    if birthday_from:

        sql += """
            AND birthday >= %s
        """

        params.append(birthday_from)

    if birthday_to:

        sql += """
            AND birthday <= %s
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

    return templates.TemplateResponse(
        name="display.html",
        request = request,
        context={
            "records": records,
            "keyword": keyword,
            "birthday_from": birthday_from,
            "birthday_to": birthday_to
        }
    )

# ============================
# 詳細表示
# ============================
@app.get("/detail/{id}")
def detail(id: int, request: Request):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM addresses
        WHERE id = %s
    """, (id,))

    record = cur.fetchone()

    conn.close()

    return templates.TemplateResponse(
        name="detail.html",
        request=request,
        context={
            "record": record
        }
    )

# ============================
# 登録 GET
# ============================
@app.get("/register")
def register_get(request: Request):

    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={
            "request": request
        }
    )

# ============================
# 登録 POST
# ============================
@app.post("/register")
async def register_post(
        name: str = Form(...),
        kana: str = Form(...),
        age: int = Form(...),
        birthday: str = Form(...),
        gender: str = Form(...),
        blood_type: str = Form(...),
        email: str = Form(...),
        tel: str = Form(...),
        mobile: str = Form(...),
        postal_code: str = Form(...),
        address: str = Form(...),
        company: str = Form("")
    ):

    conn = get_db()
    cur = conn.cursor()

    birthday = (
        birthday
        .replace("/", "-")
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
        )VALUES(
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )""",(
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
    ))


    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/", 
        status_code=303
    )

# ============================
# CSV登録 GET
# ============================
@app.get("/register-csv")
def register_csv(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register_csv.html",
        context={}
    )

# ============================
# CSV登録 POST
# ============================
@app.post("/register-csv")
async def register_csv_post(
    csvfile: UploadFile = File(...),
    request: Request = None):

    conn = get_db()
    cur = conn.cursor()

    contents = await csvfile.read()

    reader = csv.DictReader(
        contents.decode("utf-8-sig").splitlines()
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
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
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

    return RedirectResponse(
        url="/", 
        status_code=303
    )

# ============================
# 編集画面 GET
# ============================
@app.get("/edit/{id}")
def edit_get(request: Request, id: int):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT *
    FROM addresses
    WHERE id = %s
    """, (id,))
    
    record = cur.fetchone()
    
    conn.close()
    
    return templates.TemplateResponse(
        name="edit.html",
        request=request,
        context={
            "record": record
        }
    )

# ============================
# 編集処理 POST
# ============================
@app.post("/edit/{id}")
async def edit_post(
    request: Request, 
    id: int,
    name: str = Form(...), 
    kana: str = Form(...),
    age: int = Form(...),
    birthday: str = Form(...),
    gender: str = Form(...),
    blood_type: str = Form(...),
    email: str = Form(...),
    tel: str = Form(...),
    mobile: str = Form(...),
    postal_code: str = Form(...),
    address: str = Form(...),
    company: str = Form("")   
    ):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE addresses
        SET
        name = %s,
        kana = %s,
        age = %s,
        birthday = %s,
        gender = %s,
        blood_type = %s,
        email = %s,
        tel = %s,
        mobile = %s,
        postal_code = %s,
        address = %s,
        company = %s,
        updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """, (
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
            company,
            id 
    ))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(
        url="/", 
        status_code=303
    )

# ============================
# 削除確認 GET
# ============================
@app.get("/delete/{id}")
def delete_get(request: Request, id: int):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT *
    FROM addresses
    WHERE id = %s
    """, (id,))
    
    record = cur.fetchone()
    
    conn.close()
    
    return templates.TemplateResponse(
        name="delete.html",
        request=request,
        context={
            "record": record
        }
    )

# ============================
# 削除処理 POST
# ============================
@app.post("/delete/{id}")
def delete_post(id: int):

    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
    DELETE
    FROM addresses
    WHERE id = %s
    """, (id,))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(
        url="/", 
        status_code=303
    )