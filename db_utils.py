import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Table for subject 1
cursor.execute("""
CREATE TABLE IF NOT EXISTS sub1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srn TEXT NOT NULL,
    attendance REAL DEFAULT 0.0   
)
""")

# Table for subject 2
cursor.execute("""
CREATE TABLE IF NOT EXISTS sub2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srn TEXT NOT NULL,
    attendance REAL DEFAULT 0.0
)
""")

conn.commit()
conn.close()