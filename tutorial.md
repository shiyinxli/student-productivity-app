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

## authentication & user registration
### 1. Create Pydantic Schemas(for request/response validation)
create a new file `schemas.py`
create a file `auth.py`
update `main.py` with Auth Endpoints
### test authentication system
start FastAPI backend
```
# Navigate to backend folder
cd student-productivity-app/backend

# Activate virtual environment
source venv/bin/activate  # (Mac/Linux)
# or venv\Scripts\activate  (Windows)

# Run the server
uvicorn main:app --reload
```
check if your server is working
Open your browser and go to: http://127.0.0.1:8000
You should see:
```
{"message": "Backend running"}
```
open a new terminal window
```
# Connect to your database
psql student_productivity

# List all tables (you should see 'users')
\dt

# You should see:
#         List of relations
#  Schema | Name  | Type  | Owner
# --------+-------+-------+-------
#  public | users | table | yourusername

# Exit PostgreSQL
\q
```
In a new terminal window, run:
```
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
  ```
  you should expect:
  ```
  {"id":1,"email":"test@example.com","created_at":"2024-01-01T12:00:00.123Z"}
  ```
  Verify user was created in database
  ```
  # Connect to database
psql student_productivity

# Check users table
SELECT * FROM users;

# You should see your test user with a hashed password (not "password123")
# id |      email       |         hashed_password         |         created_at
# ----+------------------+----------------------------------+----------------------------
#   1 | test@example.com | $2b$12$... (long hash string)   | 2024-01-01 12:00:00.123

# Exit
\q
```
Text login:
```
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
  ```
  Expected response:
  ```
  {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","token_type":"bearer"}
```
## requirements.txt
requirements.txt is a standard file in Python projects that lists all the dependencies (packages) your project needs to run.
```
pip freeze > requirements.txt
```