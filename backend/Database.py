import sqlite3
conn = sqlite3.connect('database.db')  # crea il database se per qualsiasi caso non esistesse già
cursor = conn.cursor()
#cursor.execute("DROP TABLE PAZIENTI")
cursor.execute("CREATE TABLE PAZIENTI (ID INT PRIMARY KEY, NOME VARCHAR(255) NOT NULL, COGNOME VARCHAR(255) NOT NULL, RESIDENZA VARCHAR(255) NOT NULL, CODICE_FISCALE VARCHAR(16) NOT NULL, DATA_NASCITA TEXT NOT NULL)")


#riempi la tabella
cursor.execute("INSERT INTO PAZIENTI (ID, NOME, COGNOME, RESIDENZA, CODICE_FISCALE, DATA_NASCITA) VALUES('1','diego','bernabini','Marte','0123456789qwerty', '2005/11/10')")
# mostra l'esempio
cursor.execute("SELECT * FROM PAZIENTI")
for row in cursor.fetchall():
    print(row)

# commit e chiudi connessione
conn.commit()
conn.close()