"""Input validation and sanitisation helpers."""
from __future__ import annotations

import re

MAX_NAME_LENGTH = 60
MAX_EMAIL_LENGTH = 254

_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}")


def is_valid_email(value: str) -> bool:
    """Return True if ``value`` looks like a valid email address."""
    candidate = (value or "").strip()
    if not candidate or len(candidate) > MAX_EMAIL_LENGTH:
        return False
    return _EMAIL_PATTERN.fullmatch(candidate) is not None


def clean_name(value: str) -> str:
    """Collapse whitespace/newlines and cap the length of a display name."""
    return " ".join((value or "").split())[:MAX_NAME_LENGTH]
