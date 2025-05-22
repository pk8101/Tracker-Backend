from .database import Session_local 
from sqlalchemy.orm import Session

def get_db():
    db: Session=Session_local()
    try:
        yield db
    finally:
        db.close()