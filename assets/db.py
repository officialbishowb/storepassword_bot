import sqlite3 as db
from datetime import date

conn = db.connect('assets/db/tg_bot.db')

def create_table():
    conn.execute('''CREATE TABLE users(
                        user_id INTEGER PRIMARY KEY,
                        stored_data_id INTEGER,
                        email TEXT,
                        password TEXT,
                        created_at DATE)
                ''')
    conn.commit()



def insert_credentials(user_id, email, password):
    """Insert a new user into the database

    Args:
        user_id (int):  id of the telegram user
        username (string): account username user wants to save
        email (string): account email the user wants to save
        password (string): account password (AES encrypted) the user wants to save
    """
    
    try:
        conn.execute('''INSERT INTO users(user_id, email, password, created_at)
                    VALUES(?, ?, ?, ?)''', (user_id, email, password, date.today()))
        conn.commit()
    except Exception:
        return False
    return True


def delete_row(user_id):
    """Delete a row from the database

    Args:
        user_id (int): id of the telegram user
    """
    conn.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    conn.commit()







if __name__ == '__main__':
    create_table()
    