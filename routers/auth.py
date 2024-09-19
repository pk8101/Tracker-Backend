from fastapi import Depends, APIRouter # type: ignore
from sqlalchemy.orm import Session
from utils.db_connection import get_db
from typing import Annotated, Optional
from pydantic import BaseModel,Field
from passlib.context import CryptContext # type: ignore
from utils.models import Users

auth_router=APIRouter()


db_dependency=Annotated[Session,Depends(get_db)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


class CreateUser(BaseModel):
    id:Optional[int]=None
    first_name:str=Field(min_length=1)
    last_name:str=Field(min_length=1)
    email:str
    password:str
    
    
@auth_router.post('/signup/')
async def user_create(create_user: CreateUser,db:db_dependency):
    if db.query(Users).filter(create_user.email==Users.email).first():
        return {"msg":"user is present"}
    Users_model=Users(first_name=create_user.first_name,
                      last_name=create_user.last_name,
                      email=create_user.email,
                      password=bcrypt_context.hash(create_user.password)
                    )
    db.add(Users_model)
    db.commit()
    
    
    
    
    
    
