import sqlite3

db_name = "attendance.db"


def init():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # table for subject 1
    cursor.execute("""
    create table if not exists mpca (
        id integer primary key autoincrement,
        srn text,
        attended integer default 0,
        max_classes integer default 20,
        timestamp DATE
    )
    """)

    # table for subject 2
    cursor.execute("""
    create table if not exists cn (
        id integer primary key autoincrement,
        srn text,
        attended integer default 0,
        max_classes integer default 25,
        timestamp DATE
    )
    """)

    conn.commit()
    conn.close()


def insert_attendance(student_info):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if student_info["subject"] == "mpca":
        cur.execute("""
            insert into mpca (srn)
            values (?)
        """, (student_info["srn"],))

    elif student_info["subject"] == "cn":
        cur.execute("""
            insert into cn (srn)
            values (?)
        """, (student_info["srn"],))

    conn.commit()
    conn.close()


def get_details(srn, subject):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    query = f"select * from {subject} where srn = ?"
    cur.execute(query, (srn,))

    result = cur.fetchall()
    conn.close()
    return result
