from src.configs.database import Base
from sqlalchemy import Column, ForeignKey,Integer, String, TIMESTAMP, func,Date

from sqlalchemy import Column
class Income(Base):
    __tablename__="income"
    _id=Column(Integer,primary_key=True,index=True)
    icon=Column(String(255))
    source=Column(String(100),nullable=False)
    amount=Column(Integer,nullable=False)
    date=Column(Date,nullable=False)
    userEmail=Column(String(100),ForeignKey("user.email"))
    created_at=Column (TIMESTAMP, default=func.now())