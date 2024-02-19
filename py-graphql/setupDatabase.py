import sqlite3

conn = sqlite3.connect('hackers.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        company TEXT,
        email TEXT,
        phone TEXT,
        UNIQUE(email)
    )
''')


# Create Skills table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill TEXT,
        rating INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')


cursor.execute('DROP TABLE IF EXISTS test;')
conn.commit()
conn.close()

