from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = "addresses"
    
    __table_args__ = {
        "sqlite_autoincrement": True
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    kana = Column(String(100))
    age = Column(Integer)
    birthday = Column(Date)
    gender = Column(String(20))
    blood_type = Column(String(20))
    email = Column(String(100))
    tel = Column(String(50))
    mobile = Column(String(50))
    postal_code = Column(String(50))
    address = Column(String(200))
    company = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )
