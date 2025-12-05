from nicegui import ui
from warewolf.data_import import crud, data_loader, db_conn
import sqlite3
from pathlib import Path

DB_FILE = "db/warewolf.db"

async def pick_folder(folder_input):
    """Open native folder picker dialog"""
    try:
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Bring dialog to front
        folder = filedialog.askdirectory(title="Select Recordings Folder")
        root.destroy()
        
        if folder:
            folder_input.value = folder
            ui.notify(f'Selected: {folder}', type='positive')
    except ImportError:
        ui.notify('tkinter not available. Please enter path manually.', type='warning')

def run_ui():
    ui.label('Warewolf Data Manager').classes('text-h4 text-bold')

    with ui.card().classes('w-full max-w-2xl'):
        ui.label('Import Recordings from Folder').classes('text-h6')
        
        with ui.row().classes('w-full items-center gap-2'):
            folder_input = ui.input('Folder path').classes('flex-grow')
            ui.button('Browse...', on_click=lambda: pick_folder(folder_input)).props('outline')
        
        data_input = ui.input('Data value (YYYY-MM-DD HH:MM:SS)')
        coords_input = ui.input('Coordinates (optional)')
        
        ui.button('Import Recordings', on_click=lambda: ui.notify(
            data_loader.import_data(DB_FILE, folder_input.value, data_input.value, coords_input.value)
        )).props('color=primary')

    # # mostra tabelle
    # recordings_table = ui.table(
    #     get_all_recordings(),
    #     columns=['ID', 'Name', 'Coordinates', 'Data']
    # )

    # sequences_table = ui.table(
    #     get_all_sequences(),
    #     columns=['ID', 'Recording ID', 'Name', 'Timestamp', 'Duration', 'Label']
    # )

    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    conn = db_conn.init_db(DB_FILE)
    if conn:
        print("Database created/existing")
        conn.close()
        run_ui()
    else:
        print("Error establishing db connection")

