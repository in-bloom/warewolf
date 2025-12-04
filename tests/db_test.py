import os
import sqlite3
import pytest

from warewolf.data_import import db_conn
from warewolf.data_import.crud import (
    insert_recordings, delete_recordings, get_recordings,
    insert_sequences, delete_sequences, get_sequences, update_sequence
)

DB_PATH = "db/test_crud.db"


@pytest.fixture()
def conn():
    # prepara directory
    dirpath = os.path.dirname(DB_PATH)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    # rimuove DB precedente
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # inizializza DB
    db_conn.init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    yield conn

    conn.close()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)



# ------------------------------------------------------------------------
# RECORDINGS CRUD
# ------------------------------------------------------------------------

def test_insert_and_get_recordings(conn):
    # records = (name, coordinates, data)
    records = [
        ("rec1", "10,20", "2024-01-01T12:00:00"),
        ("rec2", "30,40", "2024-02-01T08:00:00"),
    ]

    count = insert_recordings(conn, records)
    assert count == 2

    cur = conn.execute("SELECT id FROM recordings ORDER BY id ASC")
    ids = [row[0] for row in cur.fetchall()]

    fetched = get_recordings(conn, ids)

    assert len(fetched) == 2
    assert fetched[0][1] == "rec1"
    assert fetched[1][1] == "rec2"



def test_delete_recordings(conn):
    insert_recordings(conn, [
        ("del1", "x", "2024-01-01"),
        ("del2", "y", "2024-02-01"),
    ])

    cur = conn.execute("SELECT id FROM recordings")
    ids = [row[0] for row in cur.fetchall()]

    deleted = delete_recordings(conn, [ids[0]])
    assert deleted == 1

    remaining = get_recordings(conn, ids)
    assert len(remaining) == 1
    assert remaining[0][1] == "del2"



# ------------------------------------------------------------------------
# SEQUENCES CRUD
# ------------------------------------------------------------------------

def test_insert_and_get_sequences(conn):
    # Serve un recording per la FK
    insert_recordings(conn, [("rec", "0,0", "2024-01-01")])
    rec_id = conn.execute("SELECT id FROM recordings").fetchone()[0]

    # sequences = (recording_id, name, duration)
    # MA il nuovo schema richiede: recording_id, name, timestamp, duration, label
    sequences = [
        (rec_id, "seq1", 100, 10, None),
        (rec_id, "seq2", 200, 20, "tag"),
    ]

    count = insert_sequences(conn, sequences)
    assert count == 2

    cur = conn.execute("SELECT id FROM sequences ORDER BY id ASC")
    ids = [row[0] for row in cur.fetchall()]

    fetched = get_sequences(conn, ids)
    assert len(fetched) == 2
    assert fetched[0][2] == "seq1"
    assert fetched[0][3] == 100      # timestamp
    assert fetched[0][4] == 10       # duration

    assert fetched[1][2] == "seq2"
    assert fetched[1][5] == "tag"



def test_delete_sequences(conn):
    insert_recordings(conn, [("rec", "0,0", "2024-01-01")])
    rec_id = conn.execute("SELECT id FROM recordings").fetchone()[0]

    insert_sequences(conn, [
        (rec_id, "to_del_1", 100, 5, None),
        (rec_id, "to_del_2", 200, 7, "A"),
    ])

    cur = conn.execute("SELECT id FROM sequences")
    ids = [row[0] for row in cur.fetchall()]

    deleted = delete_sequences(conn, [ids[0]])
    assert deleted == 1

    remaining = get_sequences(conn, ids)
    assert len(remaining) == 1
    assert remaining[0][2] == "to_del_2"



def test_update_sequence(conn):
    insert_recordings(conn, [("rec", "0,0", "2024-01-01")])
    rec_id = conn.execute("SELECT id FROM recordings").fetchone()[0]

    insert_sequences(conn, [
        (rec_id, "old", 123, 5, None)
    ])

    seq_id = conn.execute("SELECT id FROM sequences").fetchone()[0]

    # aggiorno più campi
    updated = update_sequence(
        conn,
        seq_id,
        name="new",
        timestamp=999,
        duration=42,
        label="X"
    )
    assert updated == 1

    cur = conn.execute(
        "SELECT name, timestamp, duration, label FROM sequences WHERE id=?",
        (seq_id,)
    )
    name, timestamp, duration, label = cur.fetchone()

    assert name == "new"
    assert timestamp == 999
    assert duration == 42
    assert label == "X"
