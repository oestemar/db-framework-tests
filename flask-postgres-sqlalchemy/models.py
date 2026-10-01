
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Address(db.Model):
    __tablename__ = "addresses"
    
    __table_args__ = {
        "sqlite_autoincrement": True
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    kana = db.Column(db.String(100))
    age = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(20))
    email = db.Column(db.String(100))
    tel = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    address = db.Column(db.String(200))    
    company = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.now,
        onupdate=datetime.now
    )
