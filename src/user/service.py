from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, Depends, HTTPException,UploadFile,File,Request
from src.utility.emailOTP import send_otp_email
from src.security.bcryption import hashPassword,verifyPassword
from src.security.encode import createAccessToken
from ..configs.dependency import get_db 
from src.user.model import UserDetails, UserDetailsUpdate, UserLogin,VerifyOTP
from .entity import User
import pandas as pd
from http import HTTPStatus
import os,shutil
import random
from src.utility.uploadToGCP import upload_file_to_gcs

pending_registrations = dict()

class UserService:
    def userLogin(self,userLoginData: UserLogin, db:Session=Depends(get_db)):
        try:
            currentUser=db.query(User).filter(User.email==userLoginData.email).first()
            if currentUser is not None:
                if  verifyPassword(userLoginData.password,currentUser.password):
                    data={"email":currentUser.email,"id":currentUser.id}
                    token=createAccessToken(data)
                    return {"message": "User Login Success","token": token,"user":data}
                return {"message":"invalid Password try with correct password"}
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"User is not present,Please create new account")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"'{e}'")
    
    def uploadImage(self,request:Request,image,UPLOAD_DIR):
        try:
            if not image:
                raise HTTPException(status_code=400, detail="No file uploaded")
            filename = image.filename
            image.file.seek(0)  
            image_url = upload_file_to_gcs(image.file, filename, image.content_type)
            return {"imageUrl": image_url}
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"'{e}'")
        
    def createnewUser(self, userdata:UserDetails, db:Session=Depends(get_db)):
        try:
            connection=db.connection()
            SQL=f"select email from user where email='{userdata.email}'" 
            p= pd.read_sql_query(SQL, con=connection)
            if p.empty:
                newUser=User(**userdata.model_dump())
                hashpassword=hashPassword(userdata.password)
                newUser.password=hashpassword 
                db.add (newUser)
                db.commit()
                data={"email":newUser.email,"username":newUser.username}
                token=createAccessToken(data)
                return {"message": f"User '{userdata.username}' Created Successfully","token":token,"user":data}
            else:
                raise HTTPException (status_code=409, detail=f"User Already exists with email: '{userdata.email}'")
        except HTTPException as e:
            raise e
        except Exception as e:
            print (f"error while creating the user: '{e}'")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail=f"'{e}'")
        
    def deleteUser(self, email, db:Session=Depends (get_db)):
        try:
            current_user=db.query(User).filter_by(email=email).first()
            if current_user is not None: 
                db. delete(current_user)
                db. commit()
                return {"message": "User is deleted successfully"}
            else:
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN,detail=f"User is Not exists")
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"'{e}'")
        
    def userDetailsByEmail (self, email, db: Session=Depends (get_db)):
        try:
            currentUser=db.query(User).filter_by(email=email).first()
            if currentUser is not None:
                userdetails={key: value for key, value in currentUser.__dict__.items() if key!="password"}
                return userdetails
            raise HTTPException (status_code=HTTPStatus.FORBIDDEN, detail=f'user does not exists')
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus. INTERNAL_SERVER_ERROR, detail=f" {e}'")
        
    def updateUserByEmail (self, email, userData: UserDetailsUpdate, db:Session=Depends (get_db)):
        try:
            currentUser=db.query(User).filter_by(email=email).first()
            if currentUser is not None:
                currentUser.username=userData.username
                currentUser.password=hashPassword(userData.password)
                db.add(currentUser)
                db.commit()
                return {"message": "User Details updated Sucessfully"}
            raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=f"User Updation is unSuccessfull no user with email'{email}'")
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"'{e}'")
    
    def triggerEmail(self,userdata:UserDetails,background_tasks:BackgroundTasks):
        try:
            otp=str(random.randint(100000,999999))
            pending_registrations[userdata.email] = {"data": userdata, "otp": otp}
            background_tasks.add_task(send_otp_email, userdata.email, otp)
            return {"message":"OTP sent to your email. "}
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,detail=f"'{e}'")
        
    def userVeriftOTP(self,otpData:VerifyOTP):
        reg = pending_registrations.get(otpData.email)
        if not reg or reg["otp"] != otpData.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        return reg
    
    def deleteDataInMemory(self,email):
        del pending_registrations[email]
        
def get_user_service():
    return UserService()