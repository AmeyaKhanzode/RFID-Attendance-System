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
        attended INTEGER DEFAULT 0,
        max_classes INTEGER DEFAULT 20
        timestamp DATE
    )
    """)

    # Table for subject 2
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cn (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        srn TEXT,
        attended INTEGER DEFAULT 0,
        max_classes INTEGER DEFAULT 25
        timestamp DATE
    )
    """)

    conn.commit()
    conn.close()


def insert_attendance(student_info):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if student_info["subject"] == "MPCA":
        cur.execute("""
            INSERT INTO mpca (srn)
            VALUES (?)
        """, (student_info["srn"],))

    elif student_info["subject"] == "CN":
        cur.execute("""
            INSERT INTO cn (srn)
            VALUES (?)
        """, (student_info["srn"],))

    conn.commit()
    conn.close()


def get_details(srn, subject):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    query = f"SELECT * FROM {subject} WHERE SRN = ?"
    cur.execute(query, (srn,))

    result = cur.fetchall()
    conn.close()
    return result