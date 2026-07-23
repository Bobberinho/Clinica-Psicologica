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
    ID_Prescrizione: int | None
    ID_Farmaco: int
    Posologia: str
    Durata: str
class Prescrizione(BaseModel):
    ID_Paziente: int
    Data: str
    Note: str
    Lista_Dettagli: List[Dettagli_Prescrizione]
class Diagnosi(BaseModel):
    ID_Specialista:int
    ID_Paziente:int
    ID_Disturbo:int
    Stato:str
    Descrizione:str
    Data:str

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
    res = query_all_rows(token, "SELECT * FROM PAZIENTI")
    return res

@app.get("/farmaci")
def get_meds(token: str | None = Header(default=None)):
    print("GET_MEDS")
    res = query_all_rows(token,"SELECT * FROM FARMACI")
    return res

@app.get("/disturbi")
def get_conditions(token: str | None = Header(default=None)):
    print("GET_CONDITIONS")
    res = query_all_rows(token,"SELECT * FROM DISTURBI")
    return res

@app.get("/paziente/{id}/diagnosi")
def get_diagnosis(id: int, token: str | None = Header(default=None)):
    print("GET_PATIENT_DIAGNOSIS")
    res = query_all_rows(token,
         """SELECT 
                DIAGNOSI.ID AS ID_Diagnosi,
                DIAGNOSI.Stato AS Stato_Diagnosi,
                DIAGNOSI.Descrizione AS Note_Diagnosi,
                DIAGNOSI.Data AS Data_Diagnosi,
                DISTURBI.Nome AS Nome_Disturbo,
                DISTURBI.Categoria AS Categoria_Disturbo,
                DISTURBI.Descrizione AS Descrizione_Disturbo,
                SPECIALISTI.Nome AS Nome_Specialista,
                SPECIALISTI.Cognome AS Cognome_Specialista
            FROM DIAGNOSI
            JOIN PAZIENTI
                ON DIAGNOSI.ID_Paziente = PAZIENTI.ID
            JOIN DISTURBI
                ON DIAGNOSI.ID_Disturbo = DISTURBI.ID
            JOIN SPECIALISTI
                ON DIAGNOSI.ID_Specialista = SPECIALISTI.ID_Specialista
            WHERE PAZIENTI.ID = ?;""", (id,))
    return res

@app.get("/paziente/{id}/prescrizioni")
def get_prescriptions(id: int,token: str | None = Header(default=None)):
    print("GET_PATIENT_PRESCRIPTION")
    res = query_all_rows(token,
        """ SELECT 
            p.ID AS ID_Prescrizione,
            p.Data,
            p.Note AS Note_Prescrizione,
            p.ID_Psichiatra,
            s.Nome AS Nome_Psichiatra,
            s.Cognome AS Cognome_Psichiatra,
            f.ID AS ID_Farmaco,
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

@app.get("/diffusione_disturbi")
def get_mental_disorders(token: str | None = Header(default=None)):
    print("GET_MENTAL_DISORDERS")
    res=query_all_rows(token, 
        """ SELECT 
    d.Nome AS Disturbo,
    COUNT(diag.ID) AS Numero_Diagnosi,
    -- Percentuale esatta senza arrotondamento forzato
    (COUNT(diag.ID) * 1.0 / SUM(COUNT(diag.ID)) OVER()) AS Percentuale_Esatta,
    -- Percentuale arrotondata a 2 decimali
    ROUND(COUNT(diag.ID) * 1.0 / SUM(COUNT(diag.ID)) OVER(), 2) AS Percentuale
FROM DIAGNOSI diag
JOIN DISTURBI d ON diag.ID_Disturbo = d.ID
GROUP BY d.ID, d.Nome
ORDER BY Numero_Diagnosi DESC;

""")
    return res

@app.get("/numero_sedute_mese")
def get_session_count_this_month(token: str | None = Header(default=None)):
    print("GET_SESSION_COUNT")
    user = authenticate_token(token)
    conn = connect_to_db()
    cursor = conn.cursor()
    row = cursor.execute("""SELECT COUNT(*) as num from SEDUTE WHERE SEDUTE.Data BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime');""").fetchone()
    res = row["num"]
    return res

@app.get("/elenco_pazienti_con_prescrizione")
def get_patients_with_prescriptions(token: str | None = Header(default=None)):
    print("GET_PATIENTS_WITH_PRESCRIPTIONS")
    res=query_all_rows(token,
        """SELECT Nome, Cognome from PAZIENTI
        JOIN PRESCRIZIONI p
        ON PAZIENTI.ID = p.ID_Paziente
        WHERE PAZIENTI.ID = p.ID_Paziente""")
    return res

@app.post("/paziente/{id}/prescrizione")
async def create_prescription(id:int, prescrizione: Prescrizione, token: str | None = Header(default=None) ):
    print("POST_PRESCRIPTION")
    user = authenticate_token(token)
    print(user)
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO PRESCRIZIONI(ID_Paziente,ID_Psichiatra,Data,Note) VALUES(?,?,?,?)""", (id,user["ID_Specialista"], prescrizione.Data, prescrizione.Note))
        print(cursor.lastrowid)
        for dettaglio in prescrizione.Lista_Dettagli:
            cursor.execute("""INSERT INTO DETTAGLI_PRESCRIZIONE(ID_Prescrizione,ID_Farmaco,Posologia,Durata) VALUES(?,?,?,?) """,(cursor.lastrowid, dettaglio.ID_Farmaco,dettaglio.Posologia,dettaglio.Durata))
        conn.commit()
    finally:
        conn.close()

    return get_patients_with_prescriptions(id, token)

@app.post("/paziente/{id}/diagnosi")
async def create_diagnosis(id:int, diagnosi: Diagnosi, token: str | None = Header(default=None) ):
    print("POST_DIAGNOSIS")
    user = authenticate_token(token)
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO DIAGNOSI(ID_Paziente, ID_Specialista, ID_Disturbo, Stato, Descrizione, Data) VALUES(?,?,?,?,?,?)""", (id,user["ID_Specialista"], diagnosi.ID_Disturbo, diagnosi.Stato, diagnosi.Descrizione, diagnosi.Data))
        conn.commit()
    finally:
        conn.close()

    print("AGGIUNTA_DIAGNOSI")
    return {}


@app.post("/elimina_prescrizione/{id}")
async def delete_prescription(id:int, id_farmaco:int, token: str | None = Header(default=None)):
    print("DELETE_PRESCRIPTION")
    user = authenticate_token(token)
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        print(id, id_farmaco)
        cursor.execute("""DELETE FROM DETTAGLI_PRESCRIZIONE WHERE ID_Prescrizione = ? AND ID_Farmaco = ?""", (id,id_farmaco,))
        conn.commit()
    finally:
        conn.close()
    return {}

@app.post("/elimina_diagnosi/{id}")
async def delete_diagnosis(id:int, token: str | None = Header(default=None)):
    print("DELETE_DIAGNOSIS")
    user = authenticate_token(token)
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        print(id)
        cursor.execute("""DELETE FROM DIAGNOSI WHERE ID = ?""", (id))
        conn.commit()
    finally:
        conn.close()
    return {}





    
# uvicorn endpoint:app --reload