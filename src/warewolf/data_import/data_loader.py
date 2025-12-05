from .db_conn import create_connection
from .crud import insert_recordings
import os


def import_data(db_path, data_folder, data, coordinates):

    try:
        names = os.listdir(data_folder)
    except FileNotFoundError:
        return f"Folder not found: {data_folder}"

    import_list = [(name, data, coordinates) for name in names]
    if import_list == []:
        return "No data found"
    
    conn = create_connection(db_path)
    recs = insert_recordings(conn, import_list)
    conn.commit()
    conn.close()
    return f'Rows imported: {recs}'
