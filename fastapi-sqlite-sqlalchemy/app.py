import csv
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import or_
from models import Address
from datetime import datetime
import create_db
from models import Base

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_NAME = "address.db"
engine = create_engine(f"sqlite:///{DB_NAME}")

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

# ============================
# 一覧表示
# ============================
@app.get("/")
def display(request: Request):

    db = SessionLocal()

    keyword = request.query_params.get("keyword", "").strip()
    birthday_from = request.query_params.get("birthday_from", "")
    birthday_to = request.query_params.get("birthday_to", "")
    keywords = keyword.split()

    query = db.query(Address)

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

        query = query.filter(Address.birthday >= birthday_from)

    if birthday_to:

        query = query.filter(Address.birthday <= birthday_to)

    records = query.all()

    db.close()

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
def detail(request: Request, id: int):

    db = SessionLocal()
    record = db.query(Address).filter(Address.id == id).first()
    db.close()

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
        request=request,
        name="register.html",
        context={}
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

    db = SessionLocal()

    birthday = (
        birthday
        .replace("/", "-")
    )

    birthday = datetime.strptime(
        birthday,
        "%Y-%m-%d"
    ).date()

    new_address = Address(
        name=name,
        kana=kana,
        age=age,
        birthday=birthday,
        gender=gender,
        blood_type=blood_type,
        email=email,
        tel=tel,
        mobile=mobile,
        postal_code=postal_code,
        address=address,
        company=company
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    db.close()

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
    ):

    db = SessionLocal()

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

        birthday = datetime.strptime(
            birthday,
            "%Y-%m-%d"
        ).date()
        
        record = Address(
            name=row["name"],
            kana=row["kana"],
            age=int(row["age"]),
            birthday=birthday,
            gender=row["gender"],
            blood_type=row["blood_type"],
            email=row["email"],
            tel=row["tel"],
            mobile=row["mobile"],
            postal_code=row["postal_code"],
            address=row["address"],
            company=row.get("company", "")
        )
        db.add(record)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/", 
        status_code=303
    )

# ============================
# 編集画面 GET
# ============================
@app.get("/edit/{id}")
def edit_get(request: Request, id: int):

    db = SessionLocal()
    
    record = db.query(Address).filter(Address.id == id).first()
    
    db.close()
    
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

    db = SessionLocal()

    birthday = (
        datetime.strptime(
            birthday,   
            "%Y-%m-%d"
        ).date()
    )

    record = db.query(Address).filter(Address.id == id).first()

    record.name = name
    record.kana = kana
    record.age = age
    record.birthday = birthday
    record.gender = gender
    record.blood_type = blood_type
    record.email = email
    record.tel = tel
    record.mobile = mobile
    record.postal_code = postal_code
    record.address = address
    record.company = company

    db.commit()
    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )

# ============================
# 削除確認 GET
# ============================
@app.get("/delete/{id}")
def delete_get(request: Request, id: int):

    db = SessionLocal()
    
    record = db.query(Address).filter(Address.id == id).first()
    
    db.close()
    
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

    db = SessionLocal()

    record = db.query(Address).filter(Address.id == id).first()

    db.delete(record)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/", 
        status_code=303
    )

