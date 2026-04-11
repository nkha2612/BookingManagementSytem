import streamlit as st
import pandas as pd
from datetime import datetime

from services.admin_service import (
    get_all_bookings,
    delete_booking,
    update_booking
)
from services.booking_service import create_booking
from config import TABLES

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🛠️ Admin - Quản lý Booking")

# ================= LOAD DATA =================
data = get_all_bookings()

if not data:
    st.warning("⚠️ Chưa có dữ liệu")
    df = pd.DataFrame(columns=[
        "id", "customer_name", "phone", "table_id", "booking_datetime", "note"
    ])
else:
    df = pd.DataFrame(data)

# 🔥 ÉP KIỂU TRÁNH LỖI
df["id"] = pd.to_numeric(df.get("id", 0), errors="coerce")
df["phone"] = df.get("phone", "").astype(str)
df["customer_name"] = df.get("customer_name", "").astype(str)

# ================= SEARCH =================
st.subheader("🔍 Tìm kiếm")

keyword = st.text_input("Nhập tên hoặc SĐT")

if keyword:
    df = df[
        df["customer_name"].str.contains(keyword, case=False, na=False) |
        df["phone"].str.contains(keyword, na=False)
    ]

st.dataframe(df, use_container_width=True)

# ================= ADD BOOKING =================
st.subheader("➕ Thêm booking")

with st.expander("Tạo booking mới"):

    name = st.text_input("Tên", key="add_name")
    phone = st.text_input("SĐT", key="add_phone")
    table_id = st.selectbox("Bàn", TABLES, key="add_table")
    booking_time = st.datetime_input("Thời gian", key="add_time")
    note = st.text_input("Ghi chú", key="add_note")

    if st.button("Tạo"):
        success, msg = create_booking(name, phone, table_id, booking_time, note)

        if success:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

# ================= UPDATE =================
st.subheader("✏️ Sửa booking")

selected_id = st.number_input("Nhập ID cần sửa", step=1)

if selected_id:
    row = df[df["id"] == selected_id]

    if not row.empty:
        row = row.iloc[0]

        name = st.text_input("Tên", value=row["customer_name"], key="edit_name")
        phone = st.text_input("SĐT", value=row["phone"], key="edit_phone")

        table_id = st.selectbox(
            "Bàn",
            TABLES,
            index=TABLES.index(int(row["table_id"])) if str(row["table_id"]).isdigit() else 0
        )

        booking_time = st.datetime_input(
            "Thời gian",
            value=pd.to_datetime(row["booking_datetime"], errors="coerce") or datetime.now()
        )

        note = st.text_input("Ghi chú", value=row.get("note", ""))

        if st.button("Cập nhật"):
            update_booking(selected_id, name, phone, table_id, booking_time, note)
            st.success("✅ Cập nhật thành công")
            st.rerun()
    else:
        st.warning("❌ Không tìm thấy ID")

# ================= DELETE =================
st.subheader("❌ Xoá booking")

delete_id = st.number_input("Nhập ID cần xoá", step=1, key="delete_id")

if st.button("Xoá"):
    delete_booking(delete_id)
    st.success("✅ Đã xoá")
    st.rerun()