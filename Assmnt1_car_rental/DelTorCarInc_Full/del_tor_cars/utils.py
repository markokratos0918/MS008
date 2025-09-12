import hashlib
import datetime as dt
from typing import Optional
from .config import DATE_FMT


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def parse_date(s: str) -> Optional[dt.date]:
    try:
        return dt.date.fromisoformat(s)
    except Exception:
        return None


def format_date(d: dt.date) -> str:
    return d.strftime(DATE_FMT)