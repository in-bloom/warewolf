import os
import sqlite3
import pytest

from warewolf.data_import.data_loader import import_data
from warewolf.data_import.db_conn import init_db
from warewolf.data_import.crud import get_recordings

# DEBUG_DB = "db/my_test.db"

# db_path = DEBUG_DB

def test_import_data_with_files(tmp_path):
    # DB temporaneo
    db_path = tmp_path / "test.db"
    init_db(str(db_path))

    # Cartella dati temporanea
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Creo alcuni file finti
    filenames = ["a.wav", "b.wav", "c.wav"]
    for f in filenames:
        (data_folder / f).touch()

    # Valori di esempio
    coordinates = "10,20"
    data_value = "2024-01-01"

    # Eseguo import_data
    result = import_data(
        str(db_path),
        str(data_folder),
        data_value,
        coordinates
    )

    assert result == "Rows imported: 3"

    # Verifico che siano stati realmente inseriti
    conn = sqlite3.connect(str(db_path))
    rows = get_recordings(conn, [row[0] for row in conn.execute("SELECT id FROM recordings")])
    conn.close()

    assert len(rows) == 3
    names = [row[1] for row in rows]
    for f in filenames:
        assert f in names


def test_import_data_empty_folder(tmp_path):
    db_path = tmp_path / "test_empty.db"
    init_db(str(db_path))

    empty_folder = tmp_path / "empty"
    empty_folder.mkdir()

    result = import_data(
        str(db_path),
        str(empty_folder),
        "2024-01-01",
        "0,0"
    )

    assert result == "No data found"


def test_import_data_folder_not_found(tmp_path):
    db_path = tmp_path / "test_missing.db"
    init_db(str(db_path))

    missing_folder = tmp_path / "does_not_exist"

    result = import_data(
        str(db_path),
        str(missing_folder),
        "data",
        "coords"
    )

    assert "Folder not found" in result
