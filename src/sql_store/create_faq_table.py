import json
import sqlite3

with open("data/faq_data.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

conn = sqlite3.connect("data/cbnu.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        qid INTEGER PRIMARY KEY,
        question_en TEXT,
        answer_en TEXT,
        question_ko TEXT,
        answer_ko TEXT,
        question_zh TEXT,
        answer_zh TEXT,
        source TEXT
    )
""")

cursor.execute("DELETE FROM faq")

for faq in faqs:
    cursor.execute(
        """INSERT INTO faq
        (qid, question_en, answer_en, question_ko, answer_ko, question_zh, answer_zh, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            faq["qid"], faq["question_en"], faq["answer_en"],
            faq["question_ko"], faq["answer_ko"],
            faq["question_zh"], faq["answer_zh"], faq["source"]
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM faq")
count = cursor.fetchone()[0]
print(f"Inserted {count} rows into faq table.")

conn.close()