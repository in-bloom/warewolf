#!/usr/bin/env python3
"""
Script to populate the database with fake sequences for testing.
Inserts 3 sequences per recording.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root / "src"))

from warewolf.data_import import db_conn, crud
import sqlite3

DB_FILE = "db/warewolf.db"

def populate_sequences():
    """Insert 3 fake sequences per recording"""
    
    conn = db_conn.init_db(DB_FILE)
    
    # Get all recordings
    try:
        cursor = conn.execute("SELECT id FROM recordings ORDER BY id")
        recordings = cursor.fetchall()
        
        if not recordings:
            print("❌ No recordings found in database")
            conn.close()
            return
        
        print(f"Found {len(recordings)} recordings")
        
        # Generate 3 fake sequences per recording
        sequences = []
        for rec_id, in recordings:
            for i in range(3):
                # Format: (recording_id, name, timestamp, duration, label)
                name = f"seq_{rec_id}_{i+1}"
                timestamp = 100 * (i + 1)  # 100ms, 200ms, 300ms
                duration = 50 + (i * 10)    # 50ms, 60ms, 70ms
                label = None  # Start with no label
                
                sequences.append((rec_id, name, timestamp, duration, label))
        
        # Insert all sequences
        inserted = crud.insert_sequences(conn, sequences)
        conn.close()
        
        print(f"✅ Successfully inserted {inserted} sequences")
        print(f"   ({len(recordings)} recordings × 3 sequences each)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.close()

if __name__ == "__main__":
    populate_sequences()
