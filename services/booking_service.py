from models.booking_model import BookingModel
from services.availability_service import is_table_available
from services.validation_service import validate_booking


def create_booking(name, phone, table_id, booking_time, note):

    is_valid, msg = validate_booking(name, phone, booking_time)
    if not is_valid:
        return False, msg

    if not is_table_available(table_id, booking_time):
        return False, "Bàn đã được đặt"

    BookingModel.create_booking(
        name, phone, table_id, booking_time, note
    )

    return True, "Đặt bàn thành công"