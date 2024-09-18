from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from configs.database import engine, Base

app=FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



# Create all tables in the database
Base.metadata.create_all(bind=engine)


@app.get("/")
async def hello():
    return {"msg":"hello pradeep"}
