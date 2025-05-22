from passlib.context import CryptContext

bcryptContext=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password):
    return bcryptContext.hash(password)

def verifyPassword(password,hashpassword):
    return bcryptContext.verify(password,hashpassword)