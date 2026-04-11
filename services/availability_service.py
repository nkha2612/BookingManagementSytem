from datetime import timedelta, datetime


def is_table_available(table_id, booking_time, all_bookings):
    start = booking_time - timedelta(hours=3)
    end = booking_time + timedelta(hours=3)

    for booking in all_bookings:
        try:
            # parse datetime từ Google Sheets
            booking_dt = datetime.fromisoformat(booking["booking_datetime"])

            # check đúng bàn + trong khoảng thời gian
            if (
                int(booking["table_id"]) == table_id and
                start <= booking_dt <= end
            ):
                return False

        except Exception:
            continue  # tránh crash nếu dữ liệu lỗi

    return True