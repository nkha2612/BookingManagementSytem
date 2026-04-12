import streamlit as st
from datetime import datetime, date as dt_date

from models.booking_model import BookingModel
from services.booking_service import create_booking
from services.availability_service import is_table_available

from config import TABLE_VIEW, TABLE_NO_VIEW, TABLE_PRIVATE


st.set_page_config(page_title="Đặt bàn", layout="wide")

# ================= CSS =================
st.markdown("""
<style>

/* Font */
html, body, [class*="css"]  {
    font-family: 'Times New Roman', serif;
}

/* Layout */
div[data-testid="column"] {
    padding: 0px 4px !important;
}

/* Button */
button[kind="secondary"] {
    width: 100%;
    height: 75px;
    border-radius: 12px;
    margin: 4px 0;
    font-weight: bold;
    transition: 0.2s;
}

/* Hover */
button[kind="secondary"]:hover {
    transform: scale(1.05);
}

/* Disabled */
button:disabled {
    opacity: 0.4 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<h2 style='text-align:center;'>
  Đặt bàn - <span style='color:#60a5fa'>The Lăng Kính</span>
</h2>
""", unsafe_allow_html=True)

# ================= LAYOUT =================
left, right = st.columns([2,1])

# ================= FORM =================
with left:

    name = st.text_input(" Tên khách")
    phone = st.text_input(" SĐT")

    date = st.date_input(
        " Ngày",
        min_value=dt_date.today(),
        format="DD/MM/YYYY"
    )

    # TIME SLOT
    def generate_time_slots():
        slots = []
        for h in range(10, 22):
            for m in [0, 15, 30, 45]:
                if h == 21 and m > 0:
                    break
                slots.append(f"{h:02d}:{m:02d}")
        return slots

    time_str = st.selectbox("Giờ", generate_time_slots())

    hour, minute = map(int, time_str.split(":"))

    booking_time = datetime.combine(date, datetime.min.time()).replace(
        hour=hour,
        minute=minute
    )

    formatted_date = date.strftime("%d/%m/%Y")
    formatted_time = f"{hour:02d}:{minute:02d}"

    st.info(f" {formatted_date} |  {formatted_time}")

    note = st.text_input(" Yêu cầu")

# ================= ẢNH =================
with right:
    st.image("assets/restaurant.jpg", use_container_width=True)


# ================= TABLE UI =================
st.subheader(" Chọn bàn")

# ================= CHỌN KHU VỰC =================
area = st.selectbox(
    " Chọn khu vực",
    [" View kính", " Không view", " Riêng tư"]
)

# Mapping
area_map = {
    " View kính": TABLE_VIEW,
    " Không view": TABLE_NO_VIEW,
    " Riêng tư": TABLE_PRIVATE
}

selected_area_tables = area_map[area]

# ================= LỌC BÀN TRỐNG =================
# 🔥 load 1 lần
all_bookings = BookingModel.get_all()

available_tables = [
    table for table in selected_area_tables
    if is_table_available(table, booking_time, all_bookings)
]

# ================= DROPDOWN CHỌN BÀN =================
if available_tables:
    selected_table = st.selectbox(
        " Chọn bàn",
        available_tables,
        format_func=lambda x: f"Bàn {x}"
    )
else:
    selected_table = None
    st.warning(" Không còn bàn trống trong khu vực này")

# ================= HIỂN THỊ =================
if selected_table:
    st.success(f"Bạn đã chọn: Bàn {selected_table}")

# ================= SUBMIT =================
if st.button("Xác nhận đặt bàn", use_container_width=True):

    if not selected_table:
        st.error("Vui lòng chọn bàn")

    else:
        success, msg = create_booking(
            name,
            phone,
            selected_table,
            booking_time,
            note
        )

        if success:
            st.success(f"{msg} | {formatted_date} - {formatted_time}")
        else:
            st.error(msg)