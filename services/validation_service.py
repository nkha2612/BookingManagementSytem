import re
from models.booking_model import BookingModel


def validate_input(name, phone):
    if not name.strip():
        return False, "Tên không được để trống"

    if not phone.strip():
        return False, "SĐT không được để trống"

    if not re.fullmatch(r"0\d{9}", phone):
        return False, "SĐT phải 10 số và bắt đầu bằng 0"

    return True, ""


def is_phone_booked_in_day(phone, booking_time):
    count = BookingModel.count_booking_by_phone_and_date(phone, booking_time)
    return count > 0


def validate_booking(name, phone, booking_time):
    is_valid, msg = validate_input(name, phone)
    if not is_valid:
        return False, msg

    if is_phone_booked_in_day(phone, booking_time):
        return False, "SĐT này đã đặt bàn trong ngày"

    return True, "Hợp lệ"