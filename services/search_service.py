import pandas as pd
from models.booking_model import BookingModel


def search_booking(keyword):
    data = BookingModel.search(keyword)

    # ===== nếu không có dữ liệu =====
    if not data:
        return pd.DataFrame(columns=[
            "id", "customer_name", "phone",
            "table_id", "booking_datetime", "note", "combo", "dish", "table_note"
        ])

    df = pd.DataFrame(data)

    # ===== đảm bảo đủ cột =====
    expected_cols = [
        "id", "customer_name", "phone",
        "table_id", "booking_datetime", "note", "combo", "dish", "table_note"
    ]

    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    df = df[expected_cols]

    # ================= FORMAT PHONE =================
    df["phone"] = df["phone"].apply(
        lambda x: str(int(x)).zfill(10)
        if str(x).isdigit() else str(x)
    )

    # ================= FORMAT DATETIME =================
    df["booking_datetime"] = pd.to_datetime(
        df["booking_datetime"],
        errors="coerce"
    ).dt.strftime("%d/%m/%Y %H:%M")

    return df