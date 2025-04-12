import sqlite3

DB_NAME="attendance.db"

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

def insert_packet(student_info):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if student_info["subject"] == "mpca":
        cur.execute("""
            INSERT INTO mpca()
            VALUES (?,?,?)""", (
                    ip_header_details["src_ip"],
                    ip_header_details["dest_ip"],
                    packet_details["src_port"],
                    packet_details["dest_port"],
                    str(bin(packet_details["tcp_flags"]))[2:],
                    ip_header_details["protocol"],
                    packet_details["payload"].hex()
                    ))

    elif student_info["subject"] == "cn":
        cur.execute("""
            INSERT INTO cn()
            VALUES (?,?,?)""", (
                    ip_header_details["src_ip"],
                    ip_header_details["dest_ip"],
                    packet_details["src_port"],
                    packet_details["dest_port"],
                    str(bin(packet_details["tcp_flags"]))[2:],
                    ip_header_details["protocol"],
                    packet_details["payload"].hex()
                    ))
    conn.commit()
    conn.close()
