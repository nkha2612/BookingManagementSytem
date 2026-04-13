import streamlit as st
from datetime import datetime, date as dt_date

from models.booking_model import BookingModel
from services.booking_service import create_booking
from services.availability_service import is_table_available

from config import TABLE_VIEW, TABLE_NO_VIEW, TABLE_PRIVATE

st.set_page_config(
    page_title="Đặt bàn",
    page_icon="assets/page_logo.jpg",
    layout="centered"
)

# ================= iPHONE STYLE CSS =================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f5f5f7;
}

/* Card */
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

/* Title */
.title {
    text-align: center;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    background: #007AFF;
    color: white;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: #005ecb;
}

/* Section label */
.section {
    font-weight: 600;
    margin-bottom: 5px;
}

/* Divider */
hr {
    margin: 10px 0;
}

</style>
""", unsafe_allow_html=True)




# ================= HEADER =================
st.markdown('<div class="title"> Đặt bàn - The Lăng Kính</div>', unsafe_allow_html=True)

# ================= CUSTOMER INFO =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**Thông tin khách hàng**")

    name = st.text_input("Tên khách")
    phone = st.text_input("SĐT")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= TIME =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**📅 Thời gian**")

    date = st.date_input(
        "Ngày",
        min_value=dt_date.today(),
        format="DD/MM/YYYY"
    )

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

    st.info(f"{date.strftime('%d/%m/%Y')} | {time_str}")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= NOTE =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    note = st.text_input("📝 Yêu cầu")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= COMBO =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**Combo**")

    combo_option = st.selectbox(
        "Chọn combo",
        ["Không chọn", "Combo 599", "Combo 699", "Combo 899", "Combo 1099"]
    )

    combo_qty = 1

    if combo_option != "Không chọn":
        combo_qty = st.number_input("Số lượng", min_value=1, value=1)

    if combo_option == "Không chọn":
        combo = ""
    else:
        combo_price = combo_option.replace("Combo ", "")
        combo = combo_price if combo_qty == 1 else f"{combo_price} x {combo_qty}"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= MENU =================
menu_map = {
    "🥗 Khai vị & Salad": [
        "Salad HEM: 175k",
        "Salad Trứng: 175k",
        "Salad Lườn: 185k",
        "Salad trái cây: 185k"
    ],
    "🍝 Mì": [
        "Spaghetti Bolognese: 195k",
        "Fettuccine Bacon: 195k",
        "Spaghetti Goose: 195k",
        "Crab Spaghetti: 225k"
    ],
    "🍗 Gà": [
        "Chicken Orange: 175k",
        "Herb Chicken: 175k",
        "Black Pepper Chicken: 175k"
    ],
    "🥩 Bò & Vịt": [
        "US Beef 150g: 225k",
        "US Beef 300g: 365k",
        "Goose Kumquat: 205k"
    ],
    "🐟 Hải sản": [
        "Shrimp Salt Chili: 205k",
        "Mustard Shrimp: 205k",
        "Scallops Cream: 205k",
        "Scallops Garlic: 205k",
        "Salmon Lemon Butter: 265k"
    ]
}

selected_dishes = []

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("**🍴 Món lẻ**")

    for category, dishes in menu_map.items():
        with st.expander(category):
            for dish in dishes:
                col1, col2 = st.columns([3,1])

                with col1:
                    checked = st.checkbox(dish, key=f"chk_{dish}")

                with col2:
                    qty = st.number_input("SL", min_value=1, key=f"qty_{dish}")

                if checked:
                    selected_dishes.append(f"{dish} x{qty}" if qty > 1 else dish)

    if selected_dishes:
        st.success("Đã chọn:")
        for d in selected_dishes:
            st.write(f"• {d}")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= TABLE NOTE =================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    table_note = st.text_input("Nội dung trên bảng")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= AREA =================
area = st.selectbox(
    "Khu vực ngồi",
    [" View kính", " Không view", " Riêng tư"]
)

area_map = {
    " View kính": TABLE_VIEW,
    " Không view": TABLE_NO_VIEW,
    " Riêng tư": TABLE_PRIVATE
}

all_bookings = BookingModel.get_all()

available_tables = [
    table for table in area_map[area]
    if is_table_available(table, booking_time, all_bookings)
]

if available_tables:
    selected_table = st.selectbox(
        "🪑 Chọn bàn",
        available_tables,
        format_func=lambda x: f"Bàn {x}"
    )
else:
    selected_table = None
    st.warning("Hết bàn")

# ================= SUBMIT =================
if st.button("Xác nhận đặt bàn"):

    if not selected_table:
        st.error("Vui lòng chọn bàn")

    else:
        success, msg = create_booking(
            name,
            phone,
            selected_table,
            booking_time,
            note,
            combo,
            ", ".join(selected_dishes),
            table_note
        )

        if success:
            st.success(f"{msg}")
        else:
            st.error(msg)