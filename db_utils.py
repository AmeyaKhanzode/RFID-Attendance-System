import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Table for subject 1
cursor.execute("""
CREATE TABLE IF NOT EXISTS mpca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srn TEXT,
    attended INTEGER,
    max_classes INTEGER
)
""")

# Table for subject 2
cursor.execute("""
CREATE TABLE IF NOT EXISTS cn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srn TEXT,
    attended INTEGER,
    max_classes INTEGER
)
""")

conn.commit()
conn.close()
