import pandas as pd
from config import GOOGLE_SHEET_URL

def load_data():
    df = pd.read_csv(GOOGLE_SHEET_URL)

    # Rename lại cho dễ dùng
    df.columns = [
        "timestamp",
        "customer_name",
        "phone",
        "booking_time",
        "event_date",
        "note"
    ]

    return df