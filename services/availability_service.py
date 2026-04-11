from datetime import timedelta
from models.booking_model import BookingModel


def is_table_available(table_id, booking_time):
    start = booking_time - timedelta(hours=3)
    end = booking_time + timedelta(hours=3)

    bookings = BookingModel.get_bookings_by_table_and_time(
        table_id, start, end
    )

    return len(bookings) == 0