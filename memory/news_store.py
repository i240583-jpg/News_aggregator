# Simple in-memory store for the latest news aggregation results

_results = None


def save_results(results: dict) -> None:
    """Save the provided results dict to the in‑memory store.

    Args:
        results: Dictionary containing aggregation results.
    """
    global _results
    _results = results


def get_results() -> dict | None:
    """Retrieve the stored results.

    Returns:
        The results dict if present, otherwise ``None``.
    """
    return _results


def clear_results() -> None:
    """Clear the stored results."""
    global _results
    _results = None


def has_results() -> bool:
    """Return ``True`` if results are currently stored, ``False`` otherwise."""
    return _results is not None
