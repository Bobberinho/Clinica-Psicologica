from datetime import datetime, timedelta, timezone
from typing import Any, List, Tuple

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
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Dettagli_Prescrizione(BaseModel):
    ID_Prescrizione: int
    ID_Farmaco: int
    Posologia: str
    Durata: str
class Prescrizione(BaseModel):
    ID_Paziente: int
    Data: str
    Note: str
    Lista_Dettagli: List[Dettagli_Prescrizione]

def check_pwd(email: str, password: str):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SPECIALISTI WHERE Email = ? AND Password = ?", (email,password))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(404, "Wrong email or password.")
    conn.close()
    return dict(user)

def check_email(email: str):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT s.ID_Specialista, s.Nome, s.Cognome, s.Numero_Telefono, s.Email, s.Password,
            -- Booleano: 1 se è Psichiatra, 0 se è Psicoterapeuta
            CASE 
                WHEN psi.ID_Specialista IS NOT NULL THEN 1 
                ELSE 0 
            END AS Is_Psichiatra,
            -- Stringa con il ruolo
            CASE 
                WHEN psi.ID_Specialista IS NOT NULL THEN 'psichiatra' 
                ELSE 'psicoterapeuta' 
            END AS ruolo,
            -- Informazioni specifiche delle rispettive tabelle
            psi.Numero_Iscrizione_Medici,
            pst.Albo_Psicoterapeuti
            FROM SPECIALISTI s
            LEFT JOIN PSICHIATRI psi ON s.ID_Specialista = psi.ID_Specialista
            LEFT JOIN PSICOTERAPEUTI pst ON s.ID_Specialista = pst.ID_Specialista
            WHERE s.Email = ?;""", (email,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(401, "Unauthorized: invalid email.")
    conn.close()
    return dict(user)

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

def query_single_row(token: str | None, query: str, params: Tuple[Any, ...] = ()) -> dict:
    authenticate_token(token) # può lanciare 401 exeption
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
    finally:
        conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Not found!")

    result_dict = dict(row)
    print(result_dict)
    return result_dict

def query_all_rows(token: str | None, query: str, params: Tuple[Any, ...] = ()) -> dict:
    authenticate_token(token) # può lanciare 401 exeption
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
    finally:
        conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Not found!")

    result_dict = [dict(row) for row in rows]
    print(result_dict)
    return result_dict


@app.post("/login")
async def login(email:str, password:str):
    print("LOGIN")
    user = check_pwd(email, password)
    if not user:
        print("NO USER")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user["Email"]}, expires_delta=None)
    return { "token": access_token, "type": "bearer" }

@app.get("/profilo")
async def current_user(token: str | None = Header(default=None)):
    print("GET_CURRENT_USER")
    user = authenticate_token(token)
    return user

@app.get("/paziente/{id}")
def get_patient(id: int, token: str | None = Header(default=None)):
    print("GET_PATIENT")
    res = query_single_row(token, "SELECT * FROM PAZIENTI WHERE ID = ?", (id,))
    return dict(res)

@app.get("/pazienti")
def get_patient(token: str | None = Header(default=None)):
    print("GET_PATIENTS")
    ret = query_all_rows(token, "SELECT * FROM PAZIENTI")
    return ret

@app.get("/paziente/{id}/diagnosi")
def get_diagnosi(id: int, token: str | None = Header(default=None)):
    print("GET_PATIENT_DIAGNOSIS")
    res = query_all_rows(token,
         """SELECT 
        PAZIENTI.Nome AS Nome_Paziente,
        PAZIENTI.Cognome AS Cognome_Paziente,
        DIAGNOSI.Stato AS Stato_Diagnosi,
        DIAGNOSI.Descrizione AS Note_Diagnosi,
        DISTURBI.Nome AS Nome_Disturbo,
        DISTURBI.Categoria AS Categoria_Disturbo,
        DISTURBI.Descrizione AS Descrizione_Disturbo
    FROM DIAGNOSI
    JOIN PAZIENTI
        ON DIAGNOSI.ID_Paziente = PAZIENTI.ID
    JOIN DISTURBI
        ON DIAGNOSI.ID_Disturbo = DISTURBI.ID
    WHERE PAZIENTI.ID = ?;""", (id,))
    return res

@app.get("/paziente/{id}/prescrizioni")
def get_prescrizione(id:int,token: str | None = Header(default=None)):
    print("GET_PATIENT_PRESCRIPTION")
    res = query_all_rows(token,
        """ SELECT 
            p.ID AS ID_Prescrizione,
            p.Data,
            p.Note AS Note_Prescrizione,
            p.ID_Psichiatra,
            s.Nome AS Nome_Psichiatra,
            s.Cognome AS Cognome_Psichiatra,
            f.Nome AS Nome_Farmaco,
            f.Principio_Attivo,
            f.Forma_Farmaceutica,
            f.Dosaggio,
            dp.Posologia,
            dp.Durata
        FROM PRESCRIZIONI p
        JOIN DETTAGLI_PRESCRIZIONE dp 
        ON p.ID = dp.ID_Prescrizione
        JOIN FARMACI f 
            ON dp.ID_Farmaco = f.ID
        JOIN SPECIALISTI s
            ON p.ID_Psichiatra = s.ID_Specialista
        WHERE p.ID_Paziente = ?
        ORDER BY p.Data DESC;""", (id,))
    return res

@app.post("/paziente/{id}/prescrizioni")
async def create_prescription(id:int, prescrizione: Prescrizione, token: str | None = Header(default=None) ):
    print("POST_PRESCRIPTION")
    user = authenticate_token(token)
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO PRESCRIZIONI(ID_Paziente,ID_Psichiatra,Data,Note) VALUES(?,?,?,?)""", (id,user["ID_Psichiatra"], prescrizione.Data, prescrizione.Note))
        for dettaglio in prescrizione.Lista_Dettagli:
            cursor.execute("""INSERT INTO DETTAGLI_PRESCRIZIONE(ID_Prescrizione,ID_Farmaco,Posologia,Durata) VALUES(?,?,?,?) """,(dettaglio.ID_Prescrizione,dettaglio.ID_Farmaco,dettaglio.Posologia,dettaglio.Durata))
        conn.commit()
        rows = []
    finally:
        conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Not found!")






    
# uvicorn endpoint:app --reload