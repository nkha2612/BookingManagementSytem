def search_booking(df, keyword):
    keyword = str(keyword).lower()

    result = df[
        df["customer_name"].str.lower().str.contains(keyword, na=False) |
        df["phone"].astype(str).str.contains(keyword)
    ]

    return result