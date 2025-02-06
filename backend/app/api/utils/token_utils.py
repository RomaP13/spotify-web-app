from datetime import datetime, timedelta


def is_token_expired(expires_at: datetime) -> bool:
    return datetime.utcnow() >= expires_at


def calculate_expiry_duration(seconds: int) -> datetime:
    return datetime.utcnow() + timedelta(seconds=seconds)
