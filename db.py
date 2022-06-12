import sqlite3 as db
import time

conn = db.connect('bot.db')

############################ MAIN FUNCTIONS ############################
def create_tables():
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER,
                        service_name TEXT,
                        email TEXT,
                        password TEXT,
                        created_at DATE)
                ''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS master_keys(
            user_id INTEGER PRIMARY KEY,
            master_password TEXT       )''')
   
        
    conn.commit()
    
    
########


def insert_credentials(user_id, service_name, email, password):
    """Insert a new user into the database

    Args:
        user_id (int):  id of the telegram user
        username (string): account username user wants to save
        email (string): account email the user wants to save
        password (string): account password (DES encrypted) the user wants to save
    """
    
    conn.execute('''INSERT INTO users(user_id, service_name, email, password, created_at)
                VALUES(?, ?, ?, ?, ?)''', (user_id, service_name, email, password, int(time.time())))
   
        
    conn.commit()
    return True



########


def get_credentials(user_id,):
    """Get all or a single credential for the user

    Args:
        user_id (int): user id of the telegram user

    Returns:
        _type_: None if the credential does not exist or a tuple with the credential data
    """
    
    cursor = conn.execute('''SELECT service_name, email, password FROM users WHERE user_id = ? ORDER BY created_at DESC''', (user_id,))
   
        
    return cursor.fetchall()


########



def get_credential(user_id, ASC=True):
    """Get a single credential for the user in ascending or descending order

    Args:
        user_id (int): user id of the telegram user
        ASC (bool): if True, return the credentials in ascending order, else in descending order
    """
    
    cursor = conn.execute('''SELECT service_name, email, password FROM users WHERE user_id = ? ORDER BY created_at {}'''.format("ASC" if ASC  else "DESC"),(user_id,))
   
        
    return cursor.fetchone()


########



def delete_credentials(user_id, to_delete):
    """Delete all credentials for the user
    
    NOTE: I am deleting specific credentials by date (created_at).
    This is not good but as date (unix timestamp) are actually always unique, this solve the problem..

    Args:
        user_id (int): id of the telegram user
        to_delete(mixed): if it is a number, it will delete the credential with that id else it will delete all credentials
    """
    
    if(type(to_delete) == int):
        cursor = conn.execute('''
                            DELETE FROM users WHERE created_at IN 
                                (SELECT created_at FROM users WHERE user_id = ? ORDER BY created_at DESC LIMIT {},1)
                            ; '''.format(to_delete-1), (user_id, ))
        
    elif(to_delete == "all"):
        conn.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
   
        
    conn.commit()
        
    return True


############################ OTHER FUNCTIONS ############################


def master_key_exist(user_id):
    """Check if the master password exists for the user

    Args:
        user_id (int): id of the telegram user
    """
    
    cursor = conn.execute('''SELECT * FROM master_keys WHERE user_id = ?''', (user_id,))

    return cursor.fetchone() is not None


########


def save_master_password(user_id, master_password):
    """Save the master password for the user

    Args:
        user_id (int): id of the telegram user
        master_password (string): master password the user wants to save
    """
    conn.execute('''INSERT INTO master_keys (user_id, master_password)
                VALUES(?, ?)''', (user_id, master_password))
    conn.commit()
    return True


########


def get_master_key(user_id):
    """Get the master password for the user

    Args:
        user_id (int): id of the telegram user
    """
    cursor = conn.execute('''SELECT master_password FROM master_keys WHERE user_id = ?''', (user_id,))
    return cursor.fetchone()[0]


########


def get_user_ids():
    """Get user_id from master_keys table for broadcast..
    """
    cursor = conn.execute('''SELECT user_id FROM master_keys''')
    return cursor.fetchall()


if __name__ == '__main__':
    create_tables()
    