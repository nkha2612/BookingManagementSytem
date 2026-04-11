import streamlit as st
from data.data_loader import load_data
from services.search_service import search_booking

st.set_page_config(page_title="Booking Search", layout="wide")

st.title(" Booking Search (DEMO)")

# Load data
df = load_data()

# Input
keyword = st.text_input("Nhập tên hoặc số điện thoại")

# Search
if st.button("Tìm kiếm"):
    result = search_booking(df, keyword)

    st.write(f"Kết quả: {len(result)} booking")
    st.dataframe(result)