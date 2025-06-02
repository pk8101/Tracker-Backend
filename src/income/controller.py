from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.configs.dependency import get_db
from src.configs.loggingConfig import log_execution
from src.income.model import IncomeData
from src.income.service import get_income_service
from src.security.auth import get_current_user

incomeRouter=APIRouter(
    prefix="/income",
    tags=["income"]
)
incomeService=get_income_service()

@incomeRouter.post("/income_create")
@log_execution
def createNewIncomeSource(
    incomeData:IncomeData,
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return incomeService.createIncome(incomeData,email,db)

@incomeRouter.get("/income_details")
@log_execution
def showAllIncomeSource(
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return incomeService.incomeDetails(email,db)

@incomeRouter.delete("/income_delete/{id}")
@log_execution
def deleteIncomeSource(
    id:int,
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return incomeService.deleteIncome(id,email,db)

@incomeRouter.get("/income_download")
@log_execution
def downloadIncomeDetails(
    db: Session = Depends(get_db),
    email=Depends(get_current_user)
    ):
    income_data = incomeService.incomeDetails(email, db)
    return incomeService.dowloadIncome(income_data)
    
