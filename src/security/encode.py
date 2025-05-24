from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
from jose import jwt
import os

load_dotenv()


EXPIRYTIME=os.getenv("ACCESS_TOKEN_EXPIRATION_TIME")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def createAccessToken(data:dict):
    try:
        expiry=datetime.now(timezone.utc)+timedelta(minutes=int(EXPIRYTIME))
        data. update({"exp":expiry})
        token=jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        raise ValueError("Cannot able to create token!")