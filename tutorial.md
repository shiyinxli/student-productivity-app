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