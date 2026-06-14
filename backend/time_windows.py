def get_window(date, granularity="half_year", bucket_size=1):
    """
    Create time windows with flexible granularity.
    """
    year = date.year

    if granularity == "half_year":
        half = 0 if date.month <= 6 else 1
        return f"{year}_H{half}"

    if granularity == "quarter":
        quarter = (date.month - 1) // 3 + 1
        return f"{year}_Q{quarter}"

    if granularity == "monthly":
        return f"{year}_{date.month:02d}"

    if granularity == "weekly":
        week_number = date.isocalendar()[1]
        window_bucket = (week_number - 1) // bucket_size
        return f"{year}_W{window_bucket:02d}"

    if granularity == "daily":
        return f"{year}_{date.month:02d}_{date.day:02d}"

    raise ValueError(f"Unknown granularity: {granularity}")

def compute_time_windows(papers, window_weeks=1, granularity="half_year"):
    """
    Compute time windows for papers using research-aligned granularity.
    """
    if not papers:
        return papers

    for paper in papers:
        paper["window"] = get_window(
            paper["published_date"],
            granularity=granularity,
            bucket_size=window_weeks
        )

    return papers