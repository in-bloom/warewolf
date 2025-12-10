from .db_conn import create_connection
from .crud import insert_recordings
import os
import shutil
from pathlib import Path


def import_data(db_path, data_folder, data, coordinates):
    """
    Import recordings from a folder.
    
    :param db_path: path to database
    :param data_folder: source folder with audio files
    :param data: date/time string
    :param coordinates: coordinates string
    :return: result message
    """
    try:
        names = os.listdir(data_folder)
    except FileNotFoundError:
        return f"Folder not found: {data_folder}"

    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}
    audio_files = [f for f in names if Path(f).suffix.lower() in audio_extensions]
    
    if not audio_files:
        return "No audio files found"
    
    # Determine destination folder and paths
    db_path_obj = Path(db_path).resolve()
    project_root = db_path_obj.parent.parent
    dest_folder = project_root / "data" / "recordings"
    dest_folder.mkdir(parents=True, exist_ok=True)

    
    # Build import list
    import_list = []
    for filename in audio_files:
        src_path = Path(data_folder) / filename
        if not src_path.is_file():
            continue
        
        dst_path = dest_folder / filename
        shutil.copy2(str(src_path), str(dst_path))
        # Store relative path from project root
        import_list.append((filename, coordinates, data))
    
    if not import_list:
        return "No audio files to import"
    
    # Use CRUD function to insert
    conn = create_connection(db_path)
    count = insert_recordings(conn, import_list)
    conn.commit()
    conn.close()
    
    return f'Rows imported: {count}'
