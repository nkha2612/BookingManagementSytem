import pandas as pd
from models.booking_model import BookingModel


def search_booking(keyword):
    data = BookingModel.search(keyword)

    columns = ["id", "customer_name", "phone", "table_id", "booking_datetime", "note"]
    df = pd.DataFrame(data, columns=columns)

    return df