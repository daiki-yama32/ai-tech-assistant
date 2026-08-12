import sqlite3

DATABASE_NAME = 'test.db'


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

def save_question(question, answer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO questions (question, answer) 
        VALUES (?, ?)
    ''', (question, answer))


    connection.commit()
    connection.close()

def get_questions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, question, answer, 
        created_at FROM questions ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()

    connection.close()
    return rows