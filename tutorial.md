## 1. create project structure
```
student-productivity-app/
 ├── frontend/
 └── backend/
 ```
## 2. setup frontend
inside the `/frontend`
```bash
npx create-next-app@latest
```
```bash
npm run dev
```

## 3. setup backend
inside `backend/`
```bash
python -m venv venv
source venv/bin/activate #(Mac/Linux)
# or venv\Scripts\activate (Windows)

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose "passlib[bcrypt]"
```
Create `main.py`
```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}
```

Run:
```
uvicorn main:app --reload
```
Go:
http://127.0.0.1:8000

## database
```bash
psql --version
```
if not installed"
```bash
brew install postgresql
brew services start postgresql
```
then create database:
```bash
createdb student_productivity
```
test:
```bash
psql student_productivity
```
if you entered the database
type `\q` to exit

## add database configuration in Backend
inside `backend/`, create a new file: `database.py`
add:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://localhost/student_productivity"

engine = create_engine(DATABASE_URL) # connects to database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # how we talk to database

Base = declarative_base() # base class for all tables
```
## create first model (user table)
create new file: `models.py`
add:
```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```
this creates:
```bash
users
 ├── id
 ├── email
 ├── hashed_password
 └── created_at
```

## create tables automatically
go to main.py and add:
```python
from database import engine
from database import Base

Base.metadata.create_all(bind=engine)
```
now restart server:
```
uvicorn main:app --reload
```
It will automatically create the table

## verify table was created
```
psql student_productivity
```
then
```
\dt
```