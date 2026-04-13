from models.booking_model import BookingModel

def get_all_bookings():
    return BookingModel.get_all()

def delete_booking(id):
    BookingModel.delete_booking(id)

def update_booking(id, name, phone, table_id, booking_time, note, combo, dish, table_note):
    BookingModel.update_booking(
        id, name, phone, table_id, booking_time, note, combo, dish, table_note
    )