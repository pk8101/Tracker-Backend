import os
from fastapi import HTTPException
from dotenv import load_dotenv 
from jose import jwt, JWTError 
from http import HTTPStatus

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def decodeAccessToken(token: str):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN, detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    except JWTError as e:
        raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN, detail=f"Invalid token: '{e}'",
        headers={"WWw-Authenticate": "Bearer"},
        )