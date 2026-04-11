from gsheet_client import get_sheet
from datetime import datetime


class BookingModel:

    @staticmethod
    def _get_next_id(sheet):
        records = sheet.get_all_records()
        if not records:
            return 1
        return max(r["id"] for r in records) + 1

    @staticmethod
    def create_booking(name, phone, table_id, booking_time, note):
        sheet = get_sheet()

        new_id = BookingModel._get_next_id(sheet)

        sheet.append_row([
            new_id,
            name,
            phone,
            table_id,
            booking_time.strftime("%Y-%m-%d %H:%M:%S"),
            note
        ])

    @staticmethod
    def get_all():
        sheet = get_sheet()
        return sheet.get_all_records()

    @staticmethod
    def search(keyword):
        data = BookingModel.get_all()

        return [
            r for r in data
            if keyword.lower() in r["customer_name"].lower()
            or keyword in r["phone"]
        ]

    @staticmethod
    def count_booking_by_phone_and_date(phone, booking_time):
        data = BookingModel.get_all()

        target_date = booking_time.strftime("%Y-%m-%d")

        return sum(
            1 for r in data
            if r["phone"] == phone
            and r["booking_datetime"].startswith(target_date)
        )

    @staticmethod
    def get_bookings_by_table_and_time(table_id, start, end):
        data = BookingModel.get_all()

        result = []

        for r in data:
            if r["table_id"] != table_id:
                continue

            dt = datetime.strptime(
                r["booking_datetime"], "%Y-%m-%d %H:%M:%S"
            )

            if start <= dt <= end:
                result.append(r)

        return result

    @staticmethod
    def delete_booking(id):
        sheet = get_sheet()
        records = sheet.get_all_records()

        for idx, r in enumerate(records, start=2):
            if r["id"] == id:
                sheet.delete_rows(idx)
                break

    @staticmethod
    def update_booking(id, name, phone, table_id, booking_time, note):
        sheet = get_sheet()
        records = sheet.get_all_records()

        for idx, r in enumerate(records, start=2):
            if r["id"] == id:
                sheet.update(f"A{idx}:F{idx}", [[
                    id,
                    name,
                    phone,
                    table_id,
                    booking_time.strftime("%Y-%m-%d %H:%M:%S"),
                    note
                ]])
                break