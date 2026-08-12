import sqlite3

connection = sqlite3.connect('test.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')

#cursor.execute('''
#    INSERT INTO questions (question, answer) 
#    VALUES (?,?)
#''', ("pythonとは？","pythonはプログラミング言語です。"))

#connection.commit()

cursor.execute('SELECT * FROM questions')
rows = cursor.fetchall()
print(rows)

connection.close()
