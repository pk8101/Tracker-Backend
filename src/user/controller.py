from fastapi import APIRouter,BackgroundTasks, HTTPException
from src.utility.emailOTP import send_otp_email
from ..configs. dependency import get_db
from src. configs. loggingConfig import log_execution
from .model import UserDetails, UserDetailsUpdate, UserLogin, VerifyOTP
from .service import get_user_service 
from sqlalchemy.orm import Session
from fastapi import Depends,UploadFile,File,Request
from src.security.auth import get_current_user
import os
import random
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

userRouter=APIRouter (
    prefix="/user",
    tags=["user"],
)

userService=get_user_service()
pending_registrations = dict()
@userRouter.post("/login")
@log_execution
async def userLogin(
    userLoginData:UserLogin, 
    db:Session=Depends(get_db)):
    return userService.userLogin(userLoginData,db)

@userRouter.post("/upload_image")
@log_execution
async def upload_image(
    request: Request,
    image: UploadFile = File(...)):
    return userService.uploadImage(request,image,UPLOAD_DIR)

@userRouter.post("/register")
@log_execution
async def userRegister (
    userdata: UserDetails, 
    background_tasks: BackgroundTasks) :
    return userService.triggerEmail(userdata,background_tasks)

@userRouter.post("/verify-otp")
@log_execution
async def verify_otp(otpData:VerifyOTP, db: Session = Depends(get_db)):
    reg=userService.userVeriftOTP(otpData)
    userCreated=userService.createnewUser(reg["data"], db)
    userService.deleteDataInMemory(otpData.email)
    return userCreated

@userRouter.get("/user_data")
@log_execution
async def userDetails(
    email:str=Depends(get_current_user), 
    db:Session=Depends (get_db)) :
  return userService.userDetailsByEmail(email,db)

@userRouter.put("/user_update/")
@log_execution
async def userUpdation (
    userData:UserDetailsUpdate,
    db:Session=Depends(get_db),
    email:str=Depends(get_current_user)):
    return userService.updateUserByEmail (email, userData,db)
    
@userRouter.delete("/user_delete/")
@log_execution
async def userDeletion(
        db:Session=Depends(get_db),
        email:str=Depends(get_current_user)):
    return userService.deleteUser (email, db)