__all__ = ["truncate"]


def truncate(s: str | None = None, max_length: int = 10) -> str:
    """
    Truncate a string to a maximum length and add "..." if it exceeds the limit.
    """
    if s is None or s == "":
        return ""
    if len(s) > max_length:
        return s[: max_length - 3] + "..."
    return s
