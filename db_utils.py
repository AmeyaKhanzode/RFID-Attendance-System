import sqlite3

DB_NAME = "attendance.db"

def init():
    conn = sqlite3.connect(DB_NAME)
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

def insert_attendance(student_info):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if student_info["subject"] == "mpca":
        cur.execute("""
            INSERT INTO mpca (srn, attended, max_classes)
            VALUES (?, ?, ?)
        """, (student_info["srn"], student_info["attended"], student_info["max_classes"]))

    elif student_info["subject"] == "cn":
        cur.execute("""
            INSERT INTO cn (srn, attended, max_classes)
            VALUES (?, ?, ?)
        """, (student_info["srn"], student_info["attended"], student_info["max_classes"]))

    conn.commit()
    conn.close()
