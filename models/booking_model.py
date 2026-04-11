import streamlit as st
from gsheet_client import get_sheet
from datetime import datetime


# ================= CACHE LAYER =================
@st.cache_data(ttl=30)
def _get_all_cached():
    sheet = get_sheet()
    return sheet.get_all_records()


class BookingModel:

    @staticmethod
    def _get_next_id(sheet):
        records = sheet.get_all_records()
        if not records:
            return 1
        return max(int(r["id"]) for r in records) + 1

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

        # 🔥 clear cache sau khi thêm
        _get_all_cached.clear()

    @staticmethod
    def get_all():
        return _get_all_cached()

    @staticmethod
    def search(keyword):
        data = BookingModel.get_all()

        keyword = str(keyword).lower()

        return [
            r for r in data
            if keyword in str(r.get("customer_name", "")).lower()
               or keyword in str(r.get("phone", ""))
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
            try:
                if int(r["table_id"]) != table_id:
                    continue

                dt = datetime.strptime(
                    r["booking_datetime"], "%Y-%m-%d %H:%M:%S"
                )

                if start <= dt <= end:
                    result.append(r)

            except Exception:
                continue

        return result

    @staticmethod
    def delete_booking(id):
        sheet = get_sheet()
        records = sheet.get_all_records()

        for idx, r in enumerate(records, start=2):
            if int(r["id"]) == id:
                sheet.delete_rows(idx)
                break

        # 🔥 clear cache
        _get_all_cached.clear()

    @staticmethod
    def update_booking(id, name, phone, table_id, booking_time, note):
        sheet = get_sheet()
        records = sheet.get_all_records()

        for idx, r in enumerate(records, start=2):
            if int(r["id"]) == id:
                sheet.update(f"A{idx}:F{idx}", [[
                    id,
                    name,
                    phone,
                    table_id,
                    booking_time.strftime("%Y-%m-%d %H:%M:%S"),
                    note
                ]])
                break

        # 🔥 clear cache
        _get_all_cached.clear()