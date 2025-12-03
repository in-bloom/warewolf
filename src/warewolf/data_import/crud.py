from .db_conn import get_cursor

def insert_recordings(conn, records):
    """records: must be a list of tuples with format (name, coordinates, data)"""

    with get_cursor(conn) as cur:
        cur.executemany(
            'INSERT INTO recordings (name, coordinates, data) VALUES (?, ?, ?)',
            records
        )
        return cur.rowcount

def delete_recordings(conn, ids):
    """
    ids: list of ids (integer)
    """
    with get_cursor(conn) as cur:
        cur.execute(
            f"DELETE FROM recordings WHERE id IN ({','.join('?' for _ in ids)})",
            ids
        )
        return cur.rowcount


def get_recordings(conn, ids):
    """
    Returns a list of tuples 
    """
    if not ids:
        return []

    placeholders = ",".join("?" for _ in ids)
    sql = f"SELECT * FROM recordings WHERE id IN ({placeholders})"

    cur = conn.execute(sql, ids)
    return cur.fetchall()

