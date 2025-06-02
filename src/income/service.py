from http import HTTPStatus
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.configs.dependency import get_db
from src.income.entity import Income
from src.income.model import IncomeData
from fastapi.responses import StreamingResponse
import pandas as pd
import io
class IncomeService:
    def createIncome(self,incomeData:IncomeData,email,db:Session=Depends(get_db)):
        try:
            newIncome=Income(**incomeData.model_dump())
            newIncome.userEmail=email
            db.add(newIncome)
            db.commit()
            return {
            "_id": newIncome._id,
            "icon": newIncome.icon,
            "source": newIncome.source,
            "amount": newIncome.amount,
            "date": str(newIncome.date),
            "userEmail": newIncome.userEmail,
            "created_at": str(newIncome.created_at)
        }
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
    
    def incomeDetails(self,email,db:Session=Depends(get_db)):
        try:
            userIncomeData=db.query(Income).filter_by(userEmail=email).all()
            return userIncomeData
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
        
    def deleteIncome(self,id,email,db:Session=Depends(get_db)):
        try:
            currentIncome=db.query(Income).filter_by(_id=id).first()
            if currentIncome is not None:
                db.delete(currentIncome)
                db.commit()
                return {"message":"Income deleted successfully"}
            return {"message":"No income source with given id to delete"}
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,detail=f"'{e}'")
        
    def dowloadIncome(self,income_data):
        data = [
        {
            "id": i._id,
            "source": i.source,
            "amount": i.amount,
            "date": i.date
        }
        for i in income_data
        ]
        # Create DataFrame
        df = pd.DataFrame(data)
        # Write to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="IncomeDetails")
        output.seek(0)
        # Return as StreamingResponse
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=income_details.xlsx"}
        )
    
def get_income_service():
    return IncomeService()