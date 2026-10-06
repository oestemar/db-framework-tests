from django.shortcuts import render, redirect
from .models import AddressBook
from django.db.models import Q
from datetime import datetime
import csv

# ============================
# 一覧表示
# ============================
def display(request):

    keyword = request.GET.get("keyword", "").strip()
    birthday_from = request.GET.get("birthday_from", "")
    birthday_to = request.GET.get("birthday_to", "")

    birthday_from = (
        birthday_from
        .replace("/", "-")
    )

    birthday_to = (
        birthday_to
        .replace("/", "-")
    )

    records = AddressBook.objects.all().order_by("id")
    keywords = keyword.split()

    for word in keywords:
        records = records.filter(
            Q(name__icontains=word) | Q(address__icontains=word)
        )

    if birthday_from:

        records = records.filter(birthday__gte=birthday_from)

    if birthday_to:

        records = records.filter(birthday__lte=birthday_to)

    return render(
        request,
        "display.html",
        {
            "records": records,
            "keyword": keyword,
            "birthday_from": birthday_from,
            "birthday_to": birthday_to
        }
    )

# ============================
# 詳細表示
# ============================
def detail(request, id):

    record = AddressBook.objects.get(id=id)

    return render(
        request,
        "detail.html",
        {
            "record": record
        }
    )

# ============================
# 登録 GET/POST
# ============================
def register(request):

    if request.method == "GET":
        return render(
            request,
            "register.html",
        )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        kana = request.POST.get("kana", "").strip()
        age = request.POST.get("age", "").strip()
        age = int(age) if age.isdigit() else None
        birthday = request.POST.get("birthday", "").strip()
        gender = request.POST.get("gender", "").strip()
        blood_type = request.POST.get("blood_type", "").strip()
        email = request.POST.get("email", "").strip()
        tel = request.POST.get("tel", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()
        address = request.POST.get("address", "").strip()
        company = request.POST.get("company", "").strip()

        birthday = (
            birthday
            .replace("/", "-")
        )

        birthday = (
            datetime.strptime(
                birthday,
                "%Y-%m-%d"
            ).date()
            if birthday else None
        )
        new_address = AddressBook(
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

        new_address.save()
        return redirect("/")

 
# ============================
# CSV登録 GET/POST
# ============================
def register_csv(request):

    if request.method == "GET":
        return render(
            request=request,
            template_name="register_csv.html",
        )

    if request.method == "POST":
        csvfile = request.FILES.get("csvfile")

        contents = csvfile.read()

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

            birthday = (
                datetime.strptime(
                    birthday,
                    "%Y-%m-%d"
                ).date()
                if birthday else None
            )

            record = AddressBook(
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

            record.save()
        return redirect("/")

# ============================
# 編集画面 GET/POST
# ============================
def edit(request, id):
    if request.method == "GET":
        
        record = AddressBook.objects.filter(id=id).first()
              
        return render(
            request,
            "edit.html",
            {
                "record": record
            }
        )

    if request.method == "POST":
        name = request.POST.get("name")
        kana = request.POST.get("kana")
        age = request.POST.get("age", "").strip()
        age = int(age) if age.isdigit() else None
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        blood_type = request.POST.get("blood_type")
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        mobile = request.POST.get("mobile")
        postal_code = request.POST.get("postal_code")
        address = request.POST.get("address")
        company = request.POST.get("company")

        record = AddressBook.objects.filter(id=id).first()

        birthday = (
            datetime.strptime(
                birthday,   
                "%Y-%m-%d"
            ).date()
            if birthday else None
        )

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

        record.save()

        return redirect("/")

# ============================
# 削除確認 GET/POST
# ============================
def delete(request, id):
    if request.method == "GET":
    
        record = AddressBook.objects.filter(id=id).first()

        return render(
            request,
            "delete.html",
            {
                "record": record
            }
        )
    
    if request.method == "POST":
        record = AddressBook.objects.filter(id=id).first()

        record.delete()

        return redirect("/")

