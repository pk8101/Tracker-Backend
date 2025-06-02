from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
from src.configs.database import * 
from src.user.controller import userRouter 
from src.income.controller import incomeRouter
from src.expense.controller import expenseRouter
from src.dashboard.controller import dashboardRouter
from src.user import entity 
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
entity.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get ("/") 
def hello():
    return {"hello": "successs running"}

app.include_router(dashboardRouter)
app.include_router(expenseRouter)
app.include_router(incomeRouter)
app.include_router(userRouter)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")