import sqlite3

DB_NAME = "attendance.db"

def init():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mpca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        srn TEXT,
        attended INTEGER DEFAULT 0,
        max_classes INTEGER DEFAULT 20
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cn (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        srn TEXT,
        attended INTEGER DEFAULT 0,
        max_classes INTEGER DEFAULT 25
    )
    """)

    conn.commit()
    conn.close()

def insert_attendance(student_info):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    subject = student_info["subject"].lower()
    if subject == "mpca":
        cur.execute("INSERT INTO mpca (srn) VALUES (?)", (student_info["srn"],))
    elif subject == "cn":
        cur.execute("INSERT INTO cn (srn) VALUES (?)", (student_info["srn"],))

    conn.commit()
    conn.close()