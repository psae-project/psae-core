from datetime import datetime
import pytz
try:
    import exchange_calendars as xcals
    NYSE = xcals.get_calendar("XNYS")
    HAS_XCALS = True
except Exception:
    HAS_XCALS = False


def utc_now() -> datetime:
    return datetime.now(pytz.utc)


def is_market_open(dt: datetime) -> bool:
    if not HAS_XCALS:
        return True
    try:
        return NYSE.is_open_on_minute(dt)
    except Exception:
        return False


def next_market_open(dt: datetime) -> datetime:
    if not HAS_XCALS:
        return dt
    return NYSE.next_open(dt)


def minutes_to_close(dt: datetime) -> int:
    if not HAS_XCALS:
        return 999
    close = NYSE.next_close(dt)
    return int((close - dt).total_seconds() / 60)
