from datetime import datetime, timedelta

REVISION_INTERVALS = [
    1,
    3,
    7,
    14,
    30,
]

def calculate_next_revision_date(
    revision_count: int,
    current_date: datetime,
) -> datetime:
    index = min(
        revision_count,
        len(REVISION_INTERVALS) - 1,
    )

    days = REVISION_INTERVALS[index]

    return current_date + timedelta(
        days=days,
    )