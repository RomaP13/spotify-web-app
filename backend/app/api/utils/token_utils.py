from datetime import datetime, timedelta, timezone


def is_token_expired(expires_at: datetime) -> bool:
    """Checks if a token has expired.

    Args:
        expires_at (datetime): The expiration date of the token.

    Returns:
        bool: True if the token has expired, False otherwise.
    """
    return datetime.now(timezone.utc) >= expires_at


def calculate_expiry_duration(seconds: int) -> datetime:
    """Calculates the expiration date based on the number of seconds.

    Args:
        seconds (int): The number of seconds for the expiration.

    Returns:
        datetime: The expiration date.
    """
    return datetime.now(timezone.utc) + timedelta(seconds=seconds)
