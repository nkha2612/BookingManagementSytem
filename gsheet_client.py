import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
@st.cache_resource
def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["GOOGLE_CREDENTIALS"],
        scopes=SCOPE
    )
    client = gspread.authorize(creds)

    for s in client.openall():
        print(s.title)

    client = gspread.authorize(creds)
    return client.open_by_key("1dcXFjGypDo2upAQEDFP3nQu5OJ77v4k78FxNlAXILwo").worksheet("bookings")