from fastapi import FastAPI 
from src.configs.database import * 
from src.user.controller import userRouter 
from src.user import entity 


app=FastAPI()
entity.Base.metadata.create_all(bind=engine)


@app.get ("/") 
def hello():
    return {"hello": "successs running"}

app.include_router(userRouter)