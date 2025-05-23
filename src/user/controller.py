from fastapi import APIRouter
from ..configs. dependency import get_db
from src. configs. loggingConfig import log_execution
from .model import UserDetails, UserDetailsUpdate, UserLogin
from .service import get_user_service 
from sqlalchemy.orm import Session
from fastapi import Depends
from src.security.auth import get_current_user

userRouter=APIRouter (
    prefix="/user",
    tags=["user"],
)

userService=get_user_service()

@userRouter.post("/login")
@log_execution
async def userLogin(
    userLoginData:UserLogin, 
    db:Session=Depends(get_db)):
    return userService.userLogin(userLoginData,db)

@userRouter.get("/")
@log_execution
async def userDetails(
    email:str=Depends(get_current_user), 
    db:Session=Depends (get_db)) :
  return userService.userDetailsByEmail(email,db)

@userRouter.post("/register")
@log_execution
async def userRegister (
    userdata: UserDetails, 
    db:Session=Depends (get_db)) :
    return userService.createnewUser(userdata, db)

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