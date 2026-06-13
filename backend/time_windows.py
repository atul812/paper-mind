def get_window(date, granularity="weekly", bucket_size=1):
    """
    Create time windows with flexible granularity.
    """
    year = date.year

    if granularity == "weekly":
        week_number = date.isocalendar()[1]
        window_bucket = (week_number - 1) // bucket_size
        return f"{year}_W{window_bucket:02d}"

    if granularity == "daily":
        return f"{year}_{date.month:02d}_{date.day:02d}"

    if granularity == "hourly":
        return f"{year}_{date.month:02d}_{date.day:02d}_H{date.hour:02d}"

    if granularity == "minute":
        return f"{year}_{date.month:02d}_{date.day:02d}_H{date.hour:02d}_M{date.minute:02d}"

    raise ValueError(f"Unknown granularity: {granularity}")

def compute_time_windows(papers, window_weeks=1):
    """
    Compute time windows for papers using dynamic granularity.
    """
    if not papers:
        return papers

    dates = [paper["published_date"] for paper in papers]
    min_date = min(dates)
    max_date = max(dates)
    total_days = (max_date.date() - min_date.date()).days
    unique_hours = len({d.hour for d in dates})
    unique_minutes = len({(d.hour, d.minute) for d in dates})

    if total_days >= 30:
        granularity = "weekly"
    elif total_days >= 7:
        granularity = "weekly"
    elif total_days >= 2:
        granularity = "daily"
    elif unique_hours > 1:
        granularity = "hourly"
    elif unique_minutes > 1:
        granularity = "minute"
    else:
        granularity = "hourly"

    for paper in papers:
        paper["window"] = get_window(
            paper["published_date"],
            granularity=granularity,
            bucket_size=window_weeks
        )

    return papers