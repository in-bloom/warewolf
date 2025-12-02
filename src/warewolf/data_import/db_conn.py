import sqlite3
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        raise(e)

def close_connection(conn):
    """ close the database connection
    :param conn: Connection object
    """
    if conn:
        conn.close()

def init_db(db_path):
    """ Check if the database file exists
    :param db_name: database file name
    :return: True if exists, False otherwise
    """
    if os.path.isfile(db_path):
        return create_connection(db_path)
    else:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn =  create_connection(db_path)
        return create_tables(conn) 
    
def create_tables(conn):
    cur = conn.cursor()
    try: 
        cur.execute('''
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            coordinates TEXT,
            data DATETIME NOT NULL
        );
    ''')
        cur.execute('''
       CREATE TABLE IF NOT EXISTS sequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recording_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            label TEXT,
            FOREIGN KEY (recording_id) REFERENCES recordings (id) ON DELETE CASCADE
        );
    ''')
    except sqlite3.Error as e:
        raise(e)
    conn.commit()
    return conn

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cur.fetchone() is not None