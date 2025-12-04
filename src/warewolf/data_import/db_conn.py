import sqlite3
import os
from contextlib import contextmanager

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    coordinates TEXT,
    data DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recording_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    label TEXT DEFAULT NULL,
    FOREIGN KEY (recording_id) REFERENCES recordings (id) ON DELETE CASCADE
);
"""
## Possibile implementazione delle impostazioni per ogni audio sequence processato
# FOREIGN KEY (settings_id) REFERENCES settings (id) ON DELETE RESTRAIN
# CREATE TABLE IF NOT EXISTS settings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT
#     campo1 TEXT
#     campo2 TEXT
#     campo3 TEXT
# );
def create_connection(db_path: str) -> sqlite3.Connection:
    """Create or open a SQLite DB and return a connection."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def init_db(db_path: str) -> sqlite3.Connection:
    """Initialize database and ensure tables exist."""
    conn = create_connection(db_path)
    with conn:
        conn.executescript(DB_SCHEMA)
    required_tables = ["recordings", "sequences"]

    for table in required_tables:
        if not table_exists(conn, table):
            raise RuntimeError(f"Errore: la tabella '{table}' non è stata creata correttamente.")

    return conn

def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """True if the table exists in DB."""
    query = """
    SELECT 1 FROM sqlite_master
    WHERE type='table' AND name=?;
    """
    cur = conn.execute(query, (table_name,))
    return cur.fetchone() is not None

@contextmanager
def get_cursor(conn):
    """Context manager for cursor handling."""
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
