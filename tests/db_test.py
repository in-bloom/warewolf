import warewolf.data_import.db_conn as db_conn
import os
DB_PATH = "db/warewolf_test.db"

def test_create_tables():
    # Remove existing test database file if it exists
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

    # Create a new database connection
    conn = db_conn.create_connection(DB_PATH)
    assert conn is not None

    # Create tables
    conn = db_conn.create_tables(conn)

    # Check that the expected tables exist
    assert db_conn.table_exists(conn, "recordings")
    assert db_conn.table_exists(conn, "sequences")

    # Clean up
    conn.close()
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

def test_init_db():
    # Remove existing test database file if it exists
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

    # Initialize the database
    conn = db_conn.init_db(DB_PATH)
    assert conn is not None
       
    # Check that the expected tables exist
    assert db_conn.table_exists(conn, "recordings")
    assert db_conn.table_exists(conn, "sequences")

    # Clean up
    conn.close()
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH) 