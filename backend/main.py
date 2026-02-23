from fastapi import FastAPI
from database import engine
from database import Base
import models

print("Tables registered:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}