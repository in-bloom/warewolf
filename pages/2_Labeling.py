import streamlit as st
from warewolf.data_import import crud, db_conn
import pandas as pd
import os

DB_FILE = "db/warewolf.db"

# Path globale ai file audio
AUDIO_BASE_PATH = "data/sequences"


def get_connection():
    """Get or create database connection"""
    if 'conn' not in st.session_state:
        st.session_state.conn = db_conn.init_db(DB_FILE)
    return st.session_state.conn


st.set_page_config(page_title="Warewolf - Labeling", layout="wide")

# Initialize connection
conn = get_connection()

try:
    # Load recordings (id, name)
    rec_rows = crud.get_recordings(conn)
    if not rec_rows:
        st.info("No recordings found. Import recordings first.")
        st.stop()

    rec_df = pd.DataFrame(rec_rows, columns=["id", "name", "coordinates", "data"])

    # Select recording
    rec_options = [f"{row['id']} - {row['name']}" for _, row in rec_df.iterrows()]
    selected_label = st.selectbox("Recording", rec_options, index=0)
    selected_rec_id = int(selected_label.split(" - ")[0])
    selected_rec = rec_df[rec_df["id"] == selected_rec_id].iloc[0]

    # Load sequences for selected recording
    seq_rows = crud.get_sequences(conn, recording_id=selected_rec_id)

    if not seq_rows:
        st.info("No sequences for this recording. Process audio first.")
        st.stop()

    df = pd.DataFrame(seq_rows, columns=["id", "recording_id", "name", "timestamp", "duration", "label"])

    # Filter unlabeled toggle
    show_unlabeled = st.checkbox("Show only unlabeled", value=True)
    if show_unlabeled:
        df = df[df["label"].isna()]
        st.caption(f"Showing {len(df)} unlabeled sequences")

    if df.empty:
        st.success("All sequences for this recording are labeled!")
        st.stop()

    # Session state index
    key_idx = f"seq_idx_{selected_rec_id}_{'unl' if show_unlabeled else 'all'}"
    if key_idx not in st.session_state:
        st.session_state[key_idx] = 0

    # Clamp index
    st.session_state[key_idx] = max(0, min(st.session_state[key_idx], len(df) - 1))

    current_row = df.iloc[st.session_state[key_idx]]

    # Player and info
    with st.container(border=True):
        st.write(f"**Sequence {st.session_state[key_idx]+1} / {len(df)}**")
        st.write(f"Recording: {selected_rec['name']} (ID {selected_rec_id})")
        st.caption(
            f"Seq ID {current_row['id']} | Name: {current_row['name']} | Duration: {current_row['duration']} ms | Timestamp: {current_row['timestamp']}"
        )

        # --- AUDIO PLAYER ---
        audio_path = os.path.join(AUDIO_BASE_PATH, f"{current_row['name']}.wav")

        if os.path.exists(audio_path):
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/wav")
        else:
            st.warning(f"Audio not found: {audio_path}")

        # Navigation
        nav_prev, nav_next = st.columns(2)
        if nav_prev.button("Prev", use_container_width=True):
            st.session_state[key_idx] = max(0, st.session_state[key_idx]-1)
            st.rerun()
        if nav_next.button("Next", use_container_width=True):
            st.session_state[key_idx] = min(len(df)-1, st.session_state[key_idx]+1)
            st.rerun()

    st.divider()

    # Label selection
    # Considera di aggiungere categorie dinamiche dal db (espandibili dall'utente) 
    categories = ["Lupo", "Capriolo", "Pecura", "Evelina Budassi", "Altro"]

    current_label = current_row['label'] if pd.notna(current_row['label']) else ""
    
    st.write("**Select Label:**")
    cols = st.columns(len(categories))
    
    for idx, category in enumerate(categories):
        with cols[idx]:
            button_type = "primary" if current_label == category else "secondary"
            if st.button(category, key=f"label_{current_row['id']}_{category}", type=button_type, use_container_width=True):
                updated = crud.update_sequence(conn, int(current_row['id']), label=category)
                if updated:
                    st.success(f"Labeled as '{category}'")
                    st.rerun()
                else:
                    st.warning("Errore nell'aggiornamento")

    # Probabilmente useless ma mantieni nel caso potesse tornare utile
    # st.caption("Jump to sequence")
    # jump_idx = st.slider("Index", 1, len(df), st.session_state[key_idx]+1)
    # if jump_idx - 1 != st.session_state[key_idx]:
    #     st.session_state[key_idx] = jump_idx - 1
    #     st.rerun()

except Exception as e:
    st.error(f"Error loading sequences: {str(e)}")
