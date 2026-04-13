import streamlit as st
import pandas as pd
from services.search_service import search_booking

st.set_page_config(page_title="Tìm kiếm Booking", page_icon="assets/page_logo.jpg", layout="centered")

st.title("Tìm kiếm Booking")

keyword = st.text_input("Nhập tên hoặc SĐT")

if st.button("Tìm"):

    if not keyword.strip():
        st.warning("⚠️ Vui lòng nhập từ khóa")
    else:
        df = search_booking(keyword)

        if not df.empty:
            st.success(f"Tìm thấy {len(df)} kết quả")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Không tìm thấy kết quả")