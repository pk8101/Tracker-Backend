from sqlalchemy import Column,Integer, String, TIMESTAMP, func

from ..configs. database import Base

class User(Base):
    __tablename__="user"
    id=Column (Integer, primary_key=True, index=True)
    username=Column (String(100), nullable=False)
    email=Column (String(100), nullable=False, unique=True)
    password=Column (String(255), nullable=False)
    role=Column (String(20), default='USER')
    created_at=Column (TIMESTAMP, default=func.now ())
