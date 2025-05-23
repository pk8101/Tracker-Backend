import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from http import HTTPStatus
from src.security.decode import decodeAccessToken

load_dotenv()

EXPIRYTIME=os.getenv("ACCESS_TOKEN_EXPIRATION_TIME")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    payload = decodeAccessToken(token)
    email = payload.get("email")
    if email is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid token",
            headers={f"WWw-Authenticate": "Bearer"},
        )
    return email