from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

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

def connect_to_db():
    conn = sqlite3.connect('database.db')
    # This allows us to access columns by name (like row['email']) instead of index (row[2])
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/utente")
def get_user(email:str, password:str):
    print("GET_USER")
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM SPECIALISTI WHERE Email = ? AND Password = ?", (email,password))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Wrong email or password")
        
    print(dict(row))
    return dict(row)

@app.get("/paziente/{id}")
def get_patient(id: int):
    print("GET_PATIENT")
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
def get_patient():
    print("GET_PATIENTS")
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