from warewolf.data_import import db_conn, crud


def test_insert_and_get_recordings(tmp_path):
	db_file = tmp_path / "test.db"
	conn = db_conn.init_db(str(db_file))

	records = [
		("rec1", "(0,0)", "2025-12-03 12:00:00"),
		("rec2", "(1,1)", "2025-12-03 13:00:00"),
	]

	inserted = crud.insert_recordings(conn, records)
	assert inserted == 2

	# fetch by ids (1 and 2)
	fetched = crud.get_recordings(conn, [1, 2])
	assert len(fetched) == 2
	# check fields for the first record
	assert fetched[0][1] == "rec1"
	assert fetched[1][1] == "rec2"

	conn.close()


def test_delete_recordings(tmp_path):
	db_file = tmp_path / "delete_test.db"
	conn = db_conn.init_db(str(db_file))

	records = [
		("a", None, "2025-01-01 00:00:00"),
		("b", None, "2025-01-02 00:00:00"),
	]
	crud.insert_recordings(conn, records)

	# verify inserted
	rows = crud.get_recordings(conn, [1, 2])
	assert len(rows) == 2

	deleted = crud.delete_recordings(conn, [1])
	assert deleted == 1

	remaining = crud.get_recordings(conn, [1, 2])
	# id 1 deleted, id 2 still present
	assert len(remaining) == 1
	assert remaining[0][0] == 2

	conn.close()


def test_get_recordings_empty_ids_returns_empty(tmp_path):
	db_file = tmp_path / "empty_ids.db"
	conn = db_conn.init_db(str(db_file))

	assert crud.get_recordings(conn, []) == []
	conn.close()
