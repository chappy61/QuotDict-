import sqlite3

DATABASE = 'data/quotes.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT,
            tags TEXT,
            note TEXT,
            favorite BOOLEAN,
            language TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ DB初期化完了")

if __name__ == '__main__':
    init_db()
