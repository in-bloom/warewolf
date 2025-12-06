from .db_conn import get_cursor

# ==== CRUD for recordings table ====
def insert_recordings(conn, records):
    """
    Docstring for insert_recordings
    
    :param conn: connection
    :param records: must be a list of tuples with format (name, coordinates, data)

    """

    with get_cursor(conn) as cur:
        cur.executemany(
            'INSERT INTO recordings (name, coordinates, data) VALUES (?, ?, ?)',
            records
        )
        return cur.rowcount

def delete_recordings(conn, ids):
    """
    Docstring for delete_recordings
    
    :param conn: connection
    :param ids: list of integers
    """
    with get_cursor(conn) as cur:
        placeholders = ','.join('?' for _ in ids)
        cur.execute(
            f"DELETE FROM recordings WHERE id IN ({placeholders})",
            ids
        )
        return cur.rowcount


def get_recordings(conn, ids=None):
    """
    Get recordings by IDs or fetch the first 10 if no IDs provided.
    
    :param conn: connection
    :param ids: list of integers (optional - if empty/None, returns first 10 recordings)
    :return: list of tuples
    """
    if not ids:
        # Return first 10 recordings when no IDs specified
        sql = "SELECT * FROM recordings ORDER BY id DESC LIMIT 10"
        cur = conn.execute(sql)
        return cur.fetchall()

    placeholders = ",".join("?" for _ in ids)
    sql = f"SELECT * FROM recordings WHERE id IN ({placeholders})"

    cur = conn.execute(sql, ids)
    return cur.fetchall()

# ==== CRUD for sequences ====

def insert_sequences(conn, sequences):
    """
    Docstring for insert_sequences
    
    :param conn: connection
    :param sequences: list of tuples with format (recording_id, name, timestamp, duration) or (recording_id, name, timestamp, duration, label)
    :return: Number of rows put into db
    :rtype: Integer
    """
    normalized = []
    for seq in sequences:
        if len(seq) == 4:
            normalized.append(seq + (None,))
        else:
            normalized.append(seq)

    with get_cursor(conn) as cur:
        # Normalize sequences to always have 5 elements (label defaults to None)
        cur.executemany(
            'INSERT INTO sequences (recording_id, name, timestamp, duration, label) VALUES (?, ?, ?, ?, ?)',
            normalized
        )
        return cur.rowcount


def delete_sequences(conn, ids):
    """
    Docstring for delete_sequences
    
    :param conn: connection
    :param ids: list of ids to delete from the db
    :return: Number of deleted rows
    :rtype: Integer
    """
    with get_cursor(conn) as cur:
        placeholders = ','.join('?' for _ in ids)
        cur.execute(
            f'DELETE FROM sequences WHERE id IN ({placeholders})',
            ids
        )
        return cur.rowcount

def get_sequences(conn, ids=None):
    """
    Docstring for get_sequences
    
    :param conn: connection
    :param ids: list of ids to get from the table
    :return: researched rows (by id)
    :rtype: list | Any
    """
    if not ids:
        sql = "SELECT * FROM sequences ORDER BY id DESC LIMIT 10"
        cur = conn.execute(sql)
        return cur.fetchall()

    placeholders = ",".join("?" for _ in ids)
    sql = f"SELECT * FROM sequences WHERE id IN ({placeholders})"

    cur = conn.execute(sql, ids)
    return cur.fetchall()
    
def update_sequence(conn, id, **fields):

    if not fields:
        return 0
    
    set_clause = ", ".join(f"{key} = ?" for key in fields.keys())
    values = list(fields.values())
    values.append(id)

    sql = f"UPDATE sequences SET {set_clause} WHERE id = ?"

    with get_cursor(conn) as cur:
        cur.execute(sql, values)
        return cur.rowcount
