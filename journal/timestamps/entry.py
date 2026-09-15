import datetime

def entry_id(value: str | None = None) -> str:
    """Generate a unique identifier for a journal entry."""
    return (value or datetime.now().strftime("%Y%m%d%H%M%S")).strip()
