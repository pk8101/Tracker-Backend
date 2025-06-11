from fastapi import APIRouter, Depends
from src.configs.dependency import Session
from src.configs.dependency import get_db
from src.configs.loggingConfig import log_execution
from src.dashboard.service import DashboardService
from src.security.auth import get_current_user

dashboardRouter=APIRouter(
    prefix="/user",
    tags=["dashboard"]
)

dashboardService=DashboardService()

@dashboardRouter.get("/dashboard")
@log_execution
def dashboardDetails(email:str=Depends(get_current_user),db:Session=Depends(get_db)):
    return dashboardService.dashboardDataUser(email,db)