import sqlite3

conn = sqlite3.connect('dati.db')
print('Opened database successfully')
c = conn.cursor()
c.execute('''
    CREATE TABLE tiku
       (question TEXT PRIMARY KEY NOT NULL,
       answer INT NOT NULL,
       answerdetail TEXT);
       ''')
print("Table created successfully")
conn.commit()
conn.close()