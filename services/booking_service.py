from models.booking_model import BookingModel, _get_all_cached
from services.availability_service import is_table_available
from services.validation_service import validate_booking


def create_booking(name, phone, table_id, booking_time, note):

    # ✅ Validate
    is_valid, msg = validate_booking(name, phone, booking_time)
    if not is_valid:
        return False, msg

    # ✅ Load data 1 lần
    all_bookings = BookingModel.get_all()

    # ✅ Check bàn
    if not is_table_available(table_id, booking_time, all_bookings):
        return False, "Bàn đã được đặt"

    # ✅ Lưu booking
    BookingModel.create_booking(
        name, phone, table_id, booking_time, note
    )

    # 🔥 Clear cache đúng chỗ
    _get_all_cached.clear()

    return True, "Đặt bàn thành công"