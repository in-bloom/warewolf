import streamlit as st
from warewolf.data_import import crud, data_loader, db_conn
from pathlib import Path
import pandas as pd
import os

DB_FILE = "db/warewolf.db"
CACHE_FILE = ".streamlit_cache.txt"

def get_connection():
    """Get or create database connection"""
    if 'conn' not in st.session_state:
        st.session_state.conn = db_conn.init_db(DB_FILE)
    return st.session_state.conn

def load_last_folder():
    """Load the last used folder from cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                folder = f.read().strip()
                if os.path.isdir(folder):
                    return folder
        except:
            pass
    return ""

def save_last_folder(folder):
    """Save the folder path to cache"""
    try:
        with open(CACHE_FILE, 'w') as f:
            f.write(folder)
    except:
        pass

def get_file_preview(folder_path):
    """Get a preview of files in the folder"""
    try:
        if not os.path.isdir(folder_path):
            return None
        
        files = list(Path(folder_path).glob('*'))
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}
        audio_files = [f for f in files if f.suffix.lower() in audio_extensions]
        
        return {
            'total_files': len(files),
            'audio_files': len(audio_files),
            'folders': len([f for f in files if f.is_dir()])
        }
    except:
        return None

st.set_page_config(page_title="Warewolf - Import", layout="wide")
st.title("📁 Import Recordings")

# Initialize connection
conn = get_connection()

# Get last used folder or use empty
last_folder = load_last_folder()

# Folder path input with autocomplete suggestions
folder_path = st.text_input(
    "Folder path",
    value=last_folder,
    placeholder="/path/to/recordings",
    help="Enter the absolute path to your recordings folder"
)

# Show folder preview
if folder_path:
    preview = get_file_preview(folder_path)
    if preview:
        st.success(f"✅ Folder valid")
        st.caption(f"📊 Preview: {preview['audio_files']} audio files, {preview['total_files']} total files")
    else:
        st.error(f"❌ Folder not found or invalid")

st.divider()

# Import form
st.subheader("Import Settings")
data_value = st.text_input(
    "Date (YYYY-MM-DD HH:MM:SS)",
    placeholder="2025-12-06 14:30:00",
    help="The date/time for this recording"
)
coords_value = st.text_input(
    "Coordinates (optional)",
    placeholder="0,0",
    help="Recording location (latitude,longitude)"
)

if st.button("🚀 Import Recordings", type="primary"):
    if folder_path and data_value:
        if not os.path.isdir(folder_path):
            st.error("❌ Invalid folder path")
        else:
            try:
                with st.spinner("Importing..."):
                    result = data_loader.import_data(DB_FILE, folder_path, data_value, coords_value or None)
                st.success(f"✅ Import completed: {result}")
                save_last_folder(folder_path)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.error("⚠️ Please fill in folder path and date")

st.divider()

# Display recordings
st.header("📋 Recent Recordings")

col1, col2 = st.columns([4, 1])

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

try:
    rows = crud.get_recordings(conn)
    
    if rows:
        # Convert tuples to dataframe
        df = pd.DataFrame(
            rows,
            columns=['ID', 'Name', 'Coordinates', 'Date']
        )
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.info("No recordings found. Import some first!")

except Exception as e:
    st.error(f"Error loading recordings: {str(e)}")
