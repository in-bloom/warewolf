import warewolf.data_import.db_conn as db_conn
import os
import sqlite3

DB_PATH = "db/warewolf_test.db"

def test_init_db():
    # ensure directory exists
    dirpath = os.path.dirname(DB_PATH)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    # remove any existing test DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # run the initialization
    db_conn.init_db(DB_PATH)

    # file created
    assert os.path.exists(DB_PATH)

    # DB contains at least one user table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recordings';")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sequences';")
    tables = cur.fetchall()
    conn.close()
    assert len(tables) > 0

    # cleanup
    os.remove(DB_PATH)
    

