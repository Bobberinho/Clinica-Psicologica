from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Default Vite/Vue dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_to_db():
    conn = sqlite3.connect('database.db')
    # This allows us to access columns by name (like row['email']) instead of index (row[2])
    conn.row_factory = sqlite3.Row
    return conn

# 2. Define your endpoint
@app.get("/users/{username}")
def get_user(username: str):
    print("called")
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Use a parameterized query (?) to prevent SQL injection
    cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="User not found xx")
        
    # Convert the SQLite row object into a standard Python dictionary to send as JSON
    return dict(row)

# uvicorn endpoint:app --reload