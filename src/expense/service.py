from http import HTTPStatus
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.configs.dependency import get_db
from fastapi.responses import StreamingResponse
from src.expense.entity import Expense
from src.expense.model import ExpenseData
import pandas as pd
import io


class ExpenseService:
    def createExpense(self,expenseData:ExpenseData,email,db:Session=Depends(get_db)):
        try:
            newExpense=Expense(**expenseData.model_dump())
            newExpense.userEmail=email
            db.add(newExpense)
            db.commit()
            return {
            "_id": newExpense._id,
            "icon": newExpense.icon,
            "category": newExpense.category,
            "amount": newExpense.amount,
            "date": str(newExpense.date),
            "userEmail": newExpense.userEmail,
            "created_at": str(newExpense.created_at)
        }
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
    
    def expenseDetails(self,email,db:Session=Depends(get_db)):
        try:
            userexpenseData=db.query(Expense).filter_by(userEmail=email).all()
            return userexpenseData
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
        
    def deleteExpense(self,id,email,db:Session=Depends(get_db)):
        try:
            currentexpense=db.query(Expense).filter_by(_id=id).first()
            if currentexpense is not None:
                db.delete(currentexpense)
                db.commit()
                return {"message":"Income deleted successfully"}
            return {"message":"No income source with given id to delete"}
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
        
    def dowloadExpense(self,expense_data):
        data = [
        {
            "id": i._id,
            "source": i.category,
            "amount": i.amount,
            "date": i.date
        }
        for i in expense_data
        ]
        # Create DataFrame
        df = pd.DataFrame(data)
        # Write to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="ExpenseDetails")
        output.seek(0)
        # Return as StreamingResponse
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=expense_details.xlsx"}
        )
    
def get_expense_service():
    return ExpenseService()