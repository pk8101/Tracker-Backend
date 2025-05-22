from fastapi import APIRouter
from ..configs. dependency import get_db
from src. configs. loggingConfig import log_execution
from .model import UserDetails, UserDetailsUpdate, UserLogin
from .service import get_user_service 
from sqlalchemy.orm import Session
from fastapi import Depends

userRouter=APIRouter (prefix="/user",
tags=["user"],
)

userService=get_user_service()

@userRouter.post("/login")
@log_execution
async def userLogin(userLoginData:UserLogin, db:Session=Depends (get_db)):
    return userService.userLogin(userLoginData,db)

@userRouter.get ("/{email}")
@log_execution
async def userDetails (email: str, db:Session=Depends (get_db)) :
  return userService.userDetailsByEmail (email,db)

@userRouter.post("/register")
@log_execution
async def userRegister (userdata: UserDetails, db:Session=Depends (get_db)) :
    return userService. createnewUser (userdata, db)

@userRouter.put("/{email}/")
@log_execution
async def userUpdation (email: str, userData:UserDetailsUpdate,db:Session=Depends(get_db)):
    return userService.updateUserByEmail (email, userData,db)
    
@userRouter.delete("/delete_user/{email}")
@log_execution
async def userDeletion (email:str, db:Session=Depends(get_db)):
    return userService.deleteUser (email, db)