import streamlit as st
import pandas as pd
from warewolf.data_import import crud, db_conn

DB_FILE = "db/warewolf.db"


def get_connection():
	"""Get or create database connection"""
	if 'conn' not in st.session_state:
		st.session_state.conn = db_conn.init_db(DB_FILE)
	return st.session_state.conn


st.set_page_config(page_title="Warewolf - Label Stats", layout="wide")
st.title("📊 Label Statistics")

conn = get_connection()

try:
	seq_rows = crud.get_sequences(conn)

	if not seq_rows:
		st.info("No sequences found. Import and process recordings first.")
	else:
		df = pd.DataFrame(
			seq_rows,
			columns=["ID", "Recording ID", "Name", "Timestamp", "Duration", "Label"]
		)

		st.subheader(f"Total Sequences: {len(df)}")

		total = len(df)
		unlabeled = len(df[df["Label"].isna()])
		labeled = len(df[df["Label"].notna()])
		progress = (labeled / total * 100) if total > 0 else 0

		col1, col2, col3 = st.columns([1, 1, 2])

		with col1:
			st.metric("Total Sequences", total)
			st.metric("Unlabeled", unlabeled)

		with col2:
			st.metric("Labeled", labeled)
			st.metric("Progress", f"{progress:.1f}%")

		with col3:
			if labeled > 0:
				st.caption("Label distribution")
				label_counts = df[df["Label"].notna()]["Label"].value_counts()
				st.bar_chart(label_counts, width="stretch")
			else:
				st.info("No labeled sequences yet")

		st.divider()

		st.subheader("All Sequences")
		st.dataframe(df, width='stretch', hide_index=True)

except Exception as e:
	st.error(f"Error loading sequences: {str(e)}")
