from database.db import get_connection


class BookingModel:

    @staticmethod
    def create_booking(name, phone, table_id, booking_time, note):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bookings (customer_name, phone, table_id, booking_datetime, note)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, table_id, booking_time, note))

        conn.commit()
        conn.close()

    @staticmethod
    def get_bookings_by_table_and_time(table_id, start, end):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM bookings
            WHERE table_id = ?
            AND booking_datetime BETWEEN ? AND ?
        """, (table_id, start, end))

        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def count_booking_by_phone_and_date(phone, booking_date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE phone = ?
            AND DATE(booking_datetime) = DATE(?)
        """, (phone, booking_date))

        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def search(keyword):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM bookings
            WHERE customer_name LIKE ?
            OR phone LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))

        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def create_booking(name, phone, table_id, booking_time, note):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                INSERT INTO bookings (customer_name, phone, table_id, booking_datetime, note)
                VALUES (?, ?, ?, ?, ?)
            """, (name, phone, table_id, booking_time, note))

        conn.commit()
        conn.close()

    # ===== READ =====
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings ORDER BY booking_datetime DESC")
        data = cursor.fetchall()

        conn.close()
        return data

    # ===== UPDATE =====
    @staticmethod
    def update_booking(id, name, phone, table_id, booking_time, note):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                UPDATE bookings
                SET customer_name=?, phone=?, table_id=?, booking_datetime=?, note=?
                WHERE id=?
            """, (name, phone, table_id, booking_time, note, id))

        conn.commit()
        conn.close()

    # ===== DELETE =====
    @staticmethod
    def delete_booking(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
        conn.commit()
        conn.close()