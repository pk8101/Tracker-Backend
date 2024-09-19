from configs.database import SessionLocal

# Dependency for getting the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
