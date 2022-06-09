import sqlite3 as db
from datetime import date
import os


conn = db.connect('assets/bot.db')

def create_tables():
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER,
                        data_id INTEGER PRIMARY KEY,
                        service_name TEXT,
                        email TEXT,
                        password TEXT,
                        created_at DATE)
                ''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS encrypt_decrypt(
              user_id INTEGER PRIMARY KEY,
              nonce BLOB,
              tag BLOB,
              master_password TEXT        )''')
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
    return True


def delete_row(user_id):
    """Delete a row from the database

    Args:
        user_id (int): id of the telegram user
    """
    conn.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    conn.commit()
    return True



if __name__ == '__main__':
    create_tables()
    