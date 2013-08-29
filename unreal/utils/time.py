# *_* coding=utf8 *_*
#!/usr/bin/env python


"""
Time related utilities and helper functions.
"""

import calendar
import datetime

import iso8601


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def isotime(at=None):
    """Stringify time in ISO 8601 format"""
    if not at:
        at = utcnow()
    str = at.strftime(TIME_FORMAT)
    tz = at.tzinfo.tzname(None) if at.tzinfo else 'UTC'
    str += ('Z' if tz == 'UTC' else tz)
    return str


def parse_isotime(timestr):
    """Parse time from ISO 8601 format"""
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(e.message)
    except TypeError as e:
        raise ValueError(e.message)


def strtime(at=None, fmt=PERFECT_TIME_FORMAT):
    """Returns formatted utcnow."""
    if not at:
        at = utcnow()
    return at.strftime(fmt)


def strtimedelta(timedelta1, format_str="{0}天{1}小时{2}分"):
    mins = int(timedelta1.seconds / 3600)
    seconds = timedelta1.seconds % 3600 / 60
    return format_str.format(timedelta1.days, mins, seconds)


def parse_strtime(timestr, fmt=PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(timestr, fmt)

def normalize_time(timestamp):
    """Normalize time in arbitrary timezone to UTC naive object"""
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset


def time_after(seconds, at=None):
    """ Get time after seconds """
    if not at:
        at = utcnow()
    timedelta = datetime.timedelta(0, seconds)
    return at + timedelta


def is_older_than(before, seconds):
    """Return True if before is older than seconds."""
    if isinstance(before, basestring):
        before = parse_strtime(before).replace(tzinfo=None)
    return utcnow() - before > datetime.timedelta(seconds=seconds)


def is_newer_than(after, seconds):
    """Return True if after is newer than seconds."""
    if isinstance(after, basestring):
        after = parse_strtime(after).replace(tzinfo=None)
    return after - utcnow() > datetime.timedelta(seconds=seconds)


def utcnow_ts():
    """Timestamp version of our utcnow function."""
    return calendar.timegm(utcnow().timetuple())


def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.utcnow()


def local_now():
    return datetime.datetime.now()


def iso8601_from_timestamp(timestamp):
    """Returns a iso8601 formated date from timestamp"""
    return isotime(datetime.datetime.utcfromtimestamp(timestamp))


utcnow.override_time = None


def set_time_override(override_time=datetime.datetime.utcnow()):
    """
    Override utils.utcnow to return a constant time or a list thereof,
    one at a time.
    """
    utcnow.override_time = override_time


def advance_time_delta(timedelta):
    """Advance overridden time using a datetime.timedelta."""
    assert(not utcnow.override_time is None)
    try:
        for dt in utcnow.override_time:
            dt += timedelta
    except TypeError:
        utcnow.override_time += timedelta


def advance_time_seconds(seconds):
    """Advance overridden time by seconds."""
    advance_time_delta(datetime.timedelta(0, seconds))


def clear_time_override():
    """Remove the overridden time."""
    utcnow.override_time = None


def marshall_now(now=None):
    """Make an rpc-safe datetime with microseconds.

    Note: tzinfo is stripped, but not required for relative times."""
    if not now:
        now = utcnow()
    return dict(day=now.day, month=now.month, year=now.year, hour=now.hour,
                minute=now.minute, second=now.second,
                microsecond=now.microsecond)


def unmarshall_time(tyme):
    """Unmarshall a datetime dict."""
    return datetime.datetime(day=tyme['day'],
                             month=tyme['month'],
                             year=tyme['year'],
                             hour=tyme['hour'],
                             minute=tyme['minute'],
                             second=tyme['second'],
                             microsecond=tyme['microsecond'])


def delta_seconds(before, after):
    """
    Compute the difference in seconds between two date, time, or
    datetime objects (as a float, to microsecond resolution).
    """
    delta = after - before
    try:
        return delta.total_seconds()
    except AttributeError:
        return ((delta.days * 24 * 3600) + delta.seconds +
                float(delta.microseconds) / (10 ** 6))


def delta_months(before, after):
    """
    算出两个日期之间相差的月份，不够一个月，则算成0, 注意：此处after > before，不做检查
    """
    months = (after.year - before.year) * 12
    months += (after.month - before.month)
    months += 0 if after.day >= before.day else -1
    return months


def is_soon(dt, window):
    """
    Determines if time is going to happen in the next window seconds.

    :params dt: the time
    :params window: minimum seconds to remain to consider the time not soon

    :return: True if expiration is within the given duration
    """
    soon = (utcnow() + datetime.timedelta(seconds=window))
    return normalize_time(dt) <= soon


def add_seconds(datetime1, seconds):
    '''
    增加秒数
    '''
    return datetime1 + datetime.timedelta(0, seconds)


def add_minutes(datetime1, minutes):
    '''
    增加分钟数
    '''
    return datetime1 + datetime.timedelta(0, minutes * 60)


def add_hours(datetime1, hours):
    '''
    增加小时数
    '''
    return datetime1 + datetime.timedelta(0, hours * 3600)


def datetime_offset_by_day(datetime1, days=1):
    return datetime1 + datetime.timedelta(days=days)


def datetime_offset_by_month(datetime1, n=1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days=1)

    # first use div and mod to determine year cycle
    q, r = divmod(datetime1.month + n, 12)

    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day

    # if input date is the last day of this month
    # then the output date should also be the last
    # day of the target month, although the day
    # may be different.
    # for example:
    # datetime1 = 8.31
    # datetime2 = 9.30
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2

    # if datetime1 day is bigger than last day of
    # target month, then, use datetime2
    # for example:
    # datetime1 = 10.31
    # datetime2 = 11.30
    if datetime1.day >= datetime2.day:
        return datetime2

    # then, here, we just replace datetime2's day
    # with the same of datetime1, that's ok.
    return datetime2.replace(day=datetime1.day)
