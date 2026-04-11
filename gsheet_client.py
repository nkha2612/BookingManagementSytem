import gspread
import streamlit as st
import json
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

    creds = Credentials.from_service_account_info(
        creds_dict, scopes=SCOPE
    )

    client = gspread.authorize(creds)
    sheet = client.open("booking").worksheet("bookings")
    return sheet