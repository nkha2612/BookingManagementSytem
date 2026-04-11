import sqlite3

def get_connection():
    return sqlite3.connect("booking.db", check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone TEXT,
        table_id INTEGER,
        booking_datetime DATETIME,
        note TEXT
    )
    """)
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_phone_date 
        ON bookings(phone, DATE(booking_datetime))
        """)

    conn.commit()
    conn.close()