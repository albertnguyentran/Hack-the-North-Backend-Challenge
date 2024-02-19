# Insert data from JSON file to database

import json
import sqlite3

def insertData():
    conn = sqlite3.connect('hackers.db')
    cursor = conn.cursor()

    with open('HTN_2023_BE_Challenge_Data.json') as file:
        data = json.load(file)

    #print(json.dumps(data, indent=2))

    for user in data:
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (name, company, email, phone)
            VALUES (?, ?, ?, ?)    
        ''', (user['name'], user['company'], user['email'], user['phone']))

        conn.commit()

        # grab id of user just added
        cursor.execute('SELECT id FROM users WHERE email = ?', (user['email'],))
        user_id = cursor.fetchone()[0]
        
        for skill in user['skills']:
            cursor.execute('''
                INSERT INTO skills (user_id, skill, rating)
                VALUES (?, ?, ?)
            ''', (user_id, skill['skill'], skill['rating']))
            conn.commit()
    
    conn.close()

if __name__ == '__main__':
    insertData()
