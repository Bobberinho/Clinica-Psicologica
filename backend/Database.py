import sqlite3
conn = sqlite3.connect('./database.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
cursor.execute("DROP TABLE EXAMPLE")
cursor.execute("CREATE TABLE EXAMPLE (NAME VARCHAR(255), SURNAME VARCHAR(255))")


#riempi la tabella
cursor.execute("INSERT INTO EXAMPLE (NAME, SURNAME) VALUES('diego','bernabini')")
# mostra l'esempio
cursor.execute("SELECT * FROM EXAMPLE")
for row in cursor.fetchall():
    print(row)

# commit e chiudi connessione
conn.commit()
conn.close()