import sqlite3
from datetime import date, timedelta

DB_NAME = "study.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        subject TEXT,
        hours REAL,
        topic TEXT,
        focus_level INTEGER
    )
""")

today = date.today()
subjects = ["DSA", "DBMS", "Web Dev", "Math", "OS"]
rows = []
for i in range(30):
    d = today - timedelta(days=i)
    subject = subjects[i % len(subjects)]
    hours = 1 + (i % 3)
    topic = f"Studied {subject} topic {i}"
    focus_level = (i % 5) + 1
    rows.append((d.isoformat(), subject, hours, topic, focus_level))

cur.executemany("""
    INSERT INTO study_sessions (date, subject, hours, topic, focus_level)
    VALUES (?, ?, ?, ?, ?)
""", rows)

conn.commit()
conn.close()
print("Done. study.db created with 30 rows.")