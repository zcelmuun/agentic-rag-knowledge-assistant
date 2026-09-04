import json
import sqlite3

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

conn = sqlite3.connect("data/cbnu.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks_metadata (
        id INTEGER PRIMARY KEY,
        language TEXT,
        section_number TEXT,
        section_title TEXT,
        source_file TEXT
    )
""")

cursor.execute("DELETE FROM chunks_metadata")

for i, chunk in enumerate(chunks):
    cursor.execute(
        "INSERT INTO chunks_metadata (id, language, section_number, section_title, source_file) VALUES (?, ?, ?, ?, ?)",
        (i, chunk["language"], chunk["section_number"], chunk["section_title"], chunk["source_file"])
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM chunks_metadata")
count = cursor.fetchone()[0]
print(f"Inserted {count} rows into chunks_metadata.")

conn.close()