import streamlit as st
from services.search_service import search_booking
from database.db import init_db

init_db()
st.title(" Tìm kiếm Booking")

keyword = st.text_input("Nhập tên hoặc SĐT")

if st.button("Tìm"):
    df = search_booking(keyword)
    st.dataframe(df)