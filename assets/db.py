import sqlite3 as db
from datetime import date
import os
import log

def drop():
    if os.path.exists("assets/bot.db"):
        os.remove("assets/bot.db")

conn = db.connect('assets/bot.db')

def create_tables():
    conn.execute('''CREATE TABLE users(
                        user_id INTEGER PRIMARY KEY,
                        data_id INTEGER,
                        service_name TEXT,
                        email TEXT,
                        password TEXT,
                        created_at DATE)
                ''')
    
    conn.execute('''CREATE TABLE master_passwords(
              user_id INTEGER PRIMARY KEY,
              master_password TEXT,
              FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
    conn.commit()


def insert_credentials(user_id, service_name, email, password):
    """Insert a new user into the database

    Args:
        user_id (int):  id of the telegram user
        username (string): account username user wants to save
        email (string): account email the user wants to save
        password (string): account password (AES encrypted) the user wants to save
    """
    
    conn.execute('''INSERT INTO users(user_id, service_name, email, password, created_at)
                VALUES(?, ?, ?, ?, ?)''', (user_id, service_name, email, password, date.today()))
    conn.commit()


def delete_row(user_id):
    """Delete a row from the database

    Args:
        user_id (int): id of the telegram user
    """
    conn.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    conn.commit()







if __name__ == '__main__':
    drop()
    create_tables()
    