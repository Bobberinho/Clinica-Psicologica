# Istruzioni per l'esecuzione dell'applicativo
Nota: sono necessarie un'installazione di Node.js e di Python.
### 1) Esecuzione del backend
Aprire un terminale nella cartella del progetto ed eseguire in ordine i seguenti comandi:
```
cd backend
python -m venv ./
Scripts\activate
python -m pip install fastapi pyjwt uvicorn
python -m uvicorn endpoint:app --reload
```
### 2) Esecuzione del frontend
Aprire un secondo terminale ed eseguire i seguenti comandi:
```
cd frontend
npm install
npm run build
npm run preview
```
Su un browser, navigare all'indirizzo: `http://localhost:4173/`
### Credenziali di Accesso
###### Accesso come psicologo:
arturo.alberti@specialisti.it
Password123

###### Accesso come psichiatra:
elena.bellini@specialisti.it
PaninoAlTonno17
