import streamlit as st
from warewolf.data_import import crud, db_conn
import pandas as pd

DB_FILE = "db/warewolf.db"

def get_connection():
    """Get or create database connection"""
    if 'conn' not in st.session_state:
        st.session_state.conn = db_conn.init_db(DB_FILE)
    return st.session_state.conn

st.set_page_config(page_title="Warewolf - Labeling", layout="wide")
st.title("🎵 Label Sequences")

# Initialize connection
conn = get_connection()

# Get all sequences
try:
    seq_rows = crud.get_sequences(conn)
    
    if not seq_rows:
        st.info("No sequences found. Import recordings and process them first.")
    else:
        # Convert to dataframe
        df = pd.DataFrame(
            seq_rows,
            columns=['ID', 'Recording ID', 'Name', 'Timestamp', 'Duration', 'Label']
        )
        
        st.subheader(f"Total Sequences: {len(df)}")
        
        # Filter by label status
        col1, col2, col3 = st.columns(3)
        with col1:
            show_unlabeled = st.checkbox("Show only unlabeled", value=True)
        
        if show_unlabeled:
            df_filtered = df[df['Label'].isna()]
            st.info(f"Showing {len(df_filtered)} unlabeled sequences")
        else:
            df_filtered = df
        
        # Display sequences in editable form
        if len(df_filtered) > 0:
            st.divider()
            
            # Predefined categories
            categories = ["Lupo", "Capriolo", "Pecura", "Evelina Budassi", "Altro"]
            
            # Display sequences one by one for labeling
            for idx, (_, row) in enumerate(df_filtered.iterrows()):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Sequence ID {row['ID']}** - Recording: {row['Recording ID']}")
                        st.caption(f"Name: {row['Name']} | Duration: {row['Duration']}ms | Timestamp: {row['Timestamp']}")
                    
                    with col2:
                        current_label = row['Label'] if pd.notna(row['Label']) else ""
                        new_label = st.selectbox(
                            "Label",
                            options=[""] + categories,
                            index=0 if not current_label else categories.index(current_label) + 1 if current_label in categories else 0,
                            key=f"label_{row['ID']}"
                        )
                    
                    if st.button("Save", key=f"save_{row['ID']}", use_container_width=True):
                        if new_label:
                            updated = crud.update_sequence(conn, row['ID'], label=new_label)
                            if updated:
                                st.success(f"Sequence {row['ID']} labeled as '{new_label}'")
                                st.rerun()
                        else:
                            st.warning("Please select a label")
        else:
            st.success("All sequences are labeled!")
        
        st.divider()
        
        # Display full table
        st.subheader("All Sequences")
        st.dataframe(df, width='stretch', hide_index=True)

except Exception as e:
    st.error(f"Error loading sequences: {str(e)}")
