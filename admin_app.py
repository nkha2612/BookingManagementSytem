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


st.set_page_config(page_title="Admin Dashboard", page_icon="assets/page_logo.jpg", layout="wide")

st.title("️Admin - Quản lý Booking")

# ================= LOAD DATA =================
data = get_all_bookings()

if not data:
    st.warning("Chưa có dữ liệu")
    df = pd.DataFrame(columns=[
        "id", "customer_name", "phone", "table_id",
        "booking_datetime", "note", "combo", "dish", "table_note"
    ])
else:
    df = pd.DataFrame(data)

# ================= FIX DATA TYPE =================
df["id"] = pd.to_numeric(df.get("id", 0), errors="coerce")
df["phone"] = df.get("phone", "").astype(str)
df["customer_name"] = df.get("customer_name", "").astype(str)

# ================= SEARCH =================
st.subheader("Tìm kiếm")

keyword = st.text_input("Nhập tên hoặc SĐT")

if keyword:
    df = df[
        df["customer_name"].str.contains(keyword, case=False, na=False) |
        df["phone"].str.contains(keyword, na=False)
    ]

st.dataframe(df, use_container_width=True)

# ================= ADD BOOKING =================
st.subheader("Thêm booking")

with st.expander("Tạo booking mới"):

    name = st.text_input("Tên", key="add_name")
    phone = st.text_input("SĐT", key="add_phone")
    table_id = st.selectbox("Bàn", TABLES, key="add_table")
    booking_time = st.datetime_input("Thời gian", key="add_time")
    note = st.text_input("Ghi chú", key="add_note")

    # ===== COMBO =====
    combo_option = st.selectbox(
        "Chọn combo",
        ["Không chọn", "Combo 599", "Combo 699", "Combo 899", "Combo 1099"],
        key="add_combo"
    )

    combo_qty = 1
    if combo_option != "Không chọn":
        combo_qty = st.number_input(
            "Số lượng combo",
            min_value=1,
            step=1,
            value=1,
            key="add_combo_qty"
        )

    if combo_option == "Không chọn":
        combo = ""
    else:
        price = combo_option.replace("Combo ", "")
        combo = price if combo_qty == 1 else f"{price} x {combo_qty}"

    # ===== MENU =====
    menu_map = {
        "🥗 Khai vị & Salad": [
            "Salad HEM: 175k", "Salad Trứng: 175k",
            "Salad Lườn: 185k", "Salad trái cây: 185k"
        ],
        "🍝 Mì": [
            "Spaghetti Bolognese: 195k", "Fettuccine Bacon: 195k",
            "Spaghetti Goose: 195k", "Crab Spaghetti: 225k"
        ],
        "🍗 Gà": [
            "Chicken Orange: 175k", "Herb Chicken: 175k",
            "Black Pepper Chicken: 175k"
        ],
        "🥩 Bò & Vịt": [
            "US Beef 150g: 225k", "US Beef 300g: 365k",
            "Goose Kumquat: 205k"
        ],
        "🐟 Hải sản": [
            "Shrimp Salt Chili: 205k", "Mustard Shrimp: 205k",
            "Scallops Cream: 205k", "Scallops Garlic: 205k",
            "Salmon Lemon Butter: 265k"
        ]
    }

    st.markdown("### 🍴 Chọn món lẻ")

    selected_dishes = []

    for category, dishes in menu_map.items():
        with st.expander(category):

            for dish in dishes:
                col1, col2 = st.columns([3, 1])

                with col1:
                    checked = st.checkbox(dish, key=f"add_chk_{dish}")

                with col2:
                    qty = st.number_input(
                        "SL",
                        min_value=1,
                        step=1,
                        key=f"add_qty_{dish}"
                    )

                if checked:
                    selected_dishes.append(
                        f"{dish} x{qty}" if qty > 1 else dish
                    )

    dish = ", ".join(selected_dishes)

    table_note = st.text_input("Nội dung bảng", key="add_table_note")

    if st.button("Tạo"):
        success, msg = create_booking(
            name, phone, table_id, booking_time,
            note, combo, dish, table_note
        )

        if success:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

# ================= UPDATE =================
st.subheader("Sửa booking")

selected_id = st.number_input("Nhập ID cần sửa", step=1)

if selected_id:
    row = df[df["id"] == selected_id]

    if not row.empty:
        row = row.iloc[0]

        name = st.text_input("Tên", value=row["customer_name"])
        phone = st.text_input("SĐT", value=row["phone"])

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

        # ===== COMBO =====
        combo_raw = str(row.get("combo", ""))

        combo_option = st.selectbox(
            "Combo",
            ["Không chọn", "Combo 599", "Combo 699", "Combo 899", "Combo 1099"]
        )

        combo_qty = st.number_input("Số lượng combo", min_value=1, value=1)

        if combo_option == "Không chọn":
            combo = ""
        else:
            price = combo_option.replace("Combo ", "")
            combo = price if combo_qty == 1 else f"{price} x {combo_qty}"

        # ===== DISH =====
        import re

        # ===== MENU =====
        menu_map = {
            "🥗 Khai vị & Salad": [
                "Salad HEM: 175k", "Salad Trứng: 175k",
                "Salad Lườn: 185k", "Salad trái cây: 185k"
            ],
            "🍝 Mì": [
                "Spaghetti Bolognese: 195k", "Fettuccine Bacon: 195k",
                "Spaghetti Goose: 195k", "Crab Spaghetti: 225k"
            ],
            "🍗 Gà": [
                "Chicken Orange: 175k", "Herb Chicken: 175k",
                "Black Pepper Chicken: 175k"
            ],
            "🥩 Bò & Vịt": [
                "US Beef 150g: 225k", "US Beef 300g: 365k",
                "Goose Kumquat: 205k"
            ],
            "🐟 Hải sản": [
                "Shrimp Salt Chili: 205k", "Mustard Shrimp: 205k",
                "Scallops Cream: 205k", "Scallops Garlic: 205k",
                "Salmon Lemon Butter: 265k"
            ]
        }

        st.markdown("### 🍴 Chỉnh sửa món lẻ")

        # ===== PARSE DATA CŨ =====
        existing_dishes = str(row.get("dish", ""))
        parsed_dishes = {}

        if existing_dishes:
            items = [i.strip() for i in existing_dishes.split(",")]

            for item in items:
                match = re.match(r"(.+?)\s*x(\d+)", item)
                if match:
                    name = match.group(1).strip()
                    qty = int(match.group(2))
                else:
                    name = item
                    qty = 1

                parsed_dishes[name] = qty

        # ===== UI =====
        selected_dishes = []

        for category, dishes in menu_map.items():
            with st.expander(category):

                for dish_item in dishes:
                    col1, col2 = st.columns([3, 1])

                    # default checked + qty
                    default_checked = dish_item in parsed_dishes
                    default_qty = parsed_dishes.get(dish_item, 1)

                    with col1:
                        checked = st.checkbox(
                            dish_item,
                            value=default_checked,
                            key=f"edit_chk_{dish_item}"
                        )

                    with col2:
                        qty = st.number_input(
                            "SL",
                            min_value=1,
                            step=1,
                            value=default_qty,
                            key=f"edit_qty_{dish_item}"
                        )

                    if checked:
                        if qty > 1:
                            selected_dishes.append(f"{dish_item} x{qty}")
                        else:
                            selected_dishes.append(dish_item)

        # ===== FINAL STRING =====
        dish = ", ".join(selected_dishes)

        # ===== PREVIEW =====
        if selected_dishes:
            st.success("Món đã chọn:")
            for d in selected_dishes:
                st.write(f"• {d}")
        table_note = st.text_input(
            "Nội dung bảng",
            value=row.get("table_note", "")
        )

        if st.button("Cập nhật"):
            update_booking(
                selected_id,
                name,
                phone,
                table_id,
                booking_time,
                note,
                combo,
                dish,
                table_note
            )
            st.success("✅ Cập nhật thành công")
            st.rerun()

# ================= DELETE =================
st.subheader("Xoá booking")

delete_id = st.number_input("Nhập ID cần xoá", step=1, key="delete_id")

if st.button("Xoá"):
    delete_booking(delete_id)
    st.success("✅ Đã xoá")
    st.rerun()