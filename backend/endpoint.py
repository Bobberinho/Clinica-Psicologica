from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from tokens import generate_token
import sqlite3

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Enable CORS
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], # Default Vite/Vue dev port
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

def check_pwd(email: str, password: str):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SPECIALISTI WHERE Email = ? AND Password = ?", (email,password))
    user = dict(cursor.fetchone())
    conn.close()
    return user

def check_email(email: str):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SPECIALISTI WHERE Email = ?", (email,))
    user = dict(cursor.fetchone())
    conn.close()
    return user

def authenticate_token(token:str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = check_email(email=email)
    if user is None:
        raise credentials_exception
    print(f"{user['Nome']} {user['Cognome']} {user['Email']}")
    return user

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt






# ENDPOINTS

def connect_to_db():
    conn = sqlite3.connect('database.db')
    # This allows us to access columns by name (like row['email']) instead of index (row[2])
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/login")
async def login(email:str, password:str):
    print("LOGIN")
    user = check_pwd(email, password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user["Email"]}, expires_delta=None)
    
    return { "token": access_token, "type": "bearer" }

@app.get("/paziente/{id}")
def get_patient(id: int, token: str | None = Header(default=None)):
    print("GET_PATIENT")
    authenticate_token(token)
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Use a parameterized query (?) to prevent SQL injection
    cursor.execute("SELECT * FROM PAZIENTI WHERE ID = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Not found!")
        
    # Convert the SQLite row object into a standard Python dictionary to send as JSON
    print(dict(row))
    return dict(row)


@app.get("/pazienti")
def get_patient(token: str | None = Header(default=None)):
    print("GET_PATIENTS")
    authenticate_token(token)
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Use a parameterized query (?) to prevent SQL injection
    cursor.execute("SELECT * FROM PAZIENTI")
    rows = cursor.fetchall()
    conn.close()
    
    if rows is None:
        raise HTTPException(status_code=404, detail="Not found!")
        
    # Convert the SQLite row object into a standard Python dictionary to send as JSON
    ret = [dict(row) for row in rows]
    print(ret)
    return ret

# uvicorn endpoint:app --reload