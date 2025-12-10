#!/usr/bin/env python3
"""
Script to populate the database with fake sequences for testing.
Inserts 5 sequences per recording.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root / "src"))

from warewolf.data_import import db_conn, crud

DB_FILE = "db/warewolf.db"

def populate_sequences():
    """Insert 5 fake sequences per recording"""
    
    conn = db_conn.init_db(DB_FILE)
    
    # Get all recordings
    try:
        cursor = conn.execute("SELECT id, name FROM recordings ORDER BY id")
        recordings = cursor.fetchall()
        
        if not recordings:
            print("❌ No recordings found in database")
            conn.close()
            return
        
        print(f"Found {len(recordings)} recordings")
        
        # Generate 5 fake sequences per recording
        sequences = []
        for rec_id, rec_name in recordings:
            for i in range(1, 6):
                # Format: (recording_id, name, timestamp, duration, label)
                name = f"{rec_name}_seq_{i}"
                timestamp = 500 * i  # 500ms, 1000ms, 1500ms, 2000ms, 2500ms
                duration = 300       # 300ms per sequenza
                label = None  # Start with no label
                
                sequences.append((rec_id, name, timestamp, duration, label))
                print(f"  + {name} (timestamp={timestamp}ms, duration={duration}ms)")
        
        # Insert all sequences
        inserted = crud.insert_sequences(conn, sequences)
        conn.commit()
        conn.close()
        
        print(f"\n✓ Inserted {inserted} sequences in DB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()

if __name__ == "__main__":
    populate_sequences()
