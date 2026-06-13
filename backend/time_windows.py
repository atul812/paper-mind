def get_window(date, months=6):
    year = date.year
    bucket = (date.month - 1) // months
    return f"{year}_W{bucket}"

def compute_time_windows(papers,window_months=6):
    for paper in papers:
        paper["window"] = get_window(
            paper["published_date"],
            window_months
        )

    return papers