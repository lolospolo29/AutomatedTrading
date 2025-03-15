from datetime import datetime, timezone


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:  # If naive, assume it's in local time and convert to UTC
        raise ValueError("Naive datetime provided, expected timezone-aware datetime")
    return dt.astimezone(timezone.utc)
