from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.configs.dependency import get_db
from src.configs.loggingConfig import log_execution
from src.expense.model import ExpenseData
from src.expense.service import get_expense_service
from src.security.auth import get_current_user

expenseRouter=APIRouter(
    prefix="/expense",
    tags=["expense"]
)
expenseService=get_expense_service()

@expenseRouter.post("/expense_create")
@log_execution
def createNewExpenseSource(
    expenseData:ExpenseData,
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return expenseService.createExpense(expenseData,email,db)

@expenseRouter.get("/expense_details")
@log_execution
def showAllExpenses(
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return expenseService.expenseDetails(email,db)

@expenseRouter.delete("/expense_delete/{id}")
@log_execution
def deleteExpenseSource(
    id:int,
    db:Session=Depends(get_db),
    email=Depends(get_current_user)):
    return expenseService.deleteExpense(id,email,db)

@expenseRouter.get("/expense_download")
@log_execution
def downloadExpenseDetails(
    db: Session = Depends(get_db),
    email=Depends(get_current_user)
    ):
    expense_data = expenseService.expenseDetails(email, db)
    return expenseService.dowloadExpense(expense_data)
    
