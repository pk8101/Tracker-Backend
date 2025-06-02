from fastapi import Depends
from src.configs.dependency import Session
from src.configs.dependency import get_db
from src.income.entity import Income
import pandas as pd


class DashboardService:
    def totalIncomes(self,email,db:Session=Depends(get_db)):
        connection=db.connection()
        SQL=f"select sum(amount) as totalamount from income where userEmail='{email}'"
        df=pd.read_sql_query(SQL,con=connection)
        totalAllIncome=df["totalamount"][0]
        return totalAllIncome
    
    def totalExpenses(self,email,db:Session=Depends(get_db)):
        connection=db.connection()
        SQL=f"select sum(amount) as totalamount from expense where userEmail='{email}'"
        df=pd.read_sql_query(SQL,con=connection)
        totalAllExpenses=df["totalamount"][0]
        return totalAllExpenses
    
    def last30DaysExpenses(self,email,db:Session=Depends(get_db)):
        connection=db.connection()
        SQL=f"select * from expense where userEmail='{email}' and date>=CURDATE() - INTERVAL 30 DAY"
        df=pd.read_sql_query(SQL,con=connection)
        transictions=[]
        total=0
        for index,data in df.iterrows():
            object={key:value for key,value in data.items()}
            total+=object["amount"]
            transictions.append(object)
        last30DaysExpenses={
            "total":total,
            "transactions":transictions
        }
        return last30DaysExpenses
    
    def last60DaysIncomes(self,email,db:Session=Depends(get_db)):
        connection=db.connection()
        SQL=f"select * from income where userEmail='{email}' and date>=CURDATE() - INTERVAL 60 DAY"
        df=pd.read_sql_query(SQL,con=connection)
        transictions=[]
        total=0
        for index,data in df.iterrows():
            object={key:value for key,value in data.items()}
            total+=object["amount"]
            transictions.append(object)
        last60DaysIncome={
            "total":total,
            "transactions":transictions
        }
        return last60DaysIncome
    
    def top10RecentTransactions(self,email,db:Session=Depends(get_db)):
        connection=db.connection()
        SQL=f"select * from expense where userEmail='{email}' and date>=CURDATE() - INTERVAL 10 DAY"
        df=pd.read_sql_query(SQL,con=connection)
        recentTransactions=[]
        for index,data in df.iterrows():
            object={key:value for key,value in data.items()}
            recentTransactions.append(object)
        return recentTransactions
        
    def dashboardDataUser(self,email,db:Session=Depends(get_db)):
        totalIncome=self.totalIncomes(email,db)
        totalExpenses=self.totalExpenses(email,db)
        totalbalance=totalIncome-totalExpenses
        last30DaysExpenses=self.last30DaysExpenses(email,db)
        last60DaysIncome=self.last60DaysIncomes(email,db)
        recentTransactions=self.top10RecentTransactions(email,db)
        data={
            "totalBalance":totalbalance,
            "totalIncome":totalIncome,
            "totalExpenses":totalExpenses,
            "last30DaysExpenses":last30DaysExpenses,
            "last60DaysIncome":last60DaysIncome,
            "recentTransactions":recentTransactions
        }
        return data
        
        