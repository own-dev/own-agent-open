"""
This module contains functions to serialize and deserialize date and time
for a unified exchange format between agents and agents_platform
"""
import datetime as dt
from datetime import datetime

import pytz

DATE_ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


def serialize_datetime(date: datetime) -> str:
    """
    Make a string representing a datetime in UTC. The resulting string
    can be deserialized by deserialize_datetime().

    If the datetime given is naive or is not in UTC, then exception is raised.

    Milliseconds can be lost in serialization.

    :param date: UTC datetime to serialize
    :return: datetime string
    """
    if date.tzinfo not in [pytz.UTC, dt.timezone.utc]:
        raise ValueError('Datetime should not be naive and should be in UTC (pytz.UTC or datetime.timezone.utc)')
    return date.strftime('%Y-%m-%dT%H:%M:%S%z')


def deserialize_datetime(date_string: str) -> datetime:
    """
    Convert a string generated by serialize_datetime() to a datetime it represents.
    The resulting datetime will be in UTC

    :param date_string: a string generated by serialize_datetime()
    :return: datetime represented by the given string
    """
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')


def datetime_from_utc_timestamp(timestamp: int) -> datetime:
    """
    Make a UTC datetime from amount of seconds since UNIX epoch in UTC
    :param timestamp: unix timestamp
    :return: datetime in UTC
    """
    return pytz.UTC.localize(datetime.utcfromtimestamp(timestamp))


def utc_epoch_datetime() -> datetime:
    """
    Unix epoch (1970 01 01) in UTC datetime
    :return: epoch UTC datetime
    """
    return datetime(1970, 1, 1, tzinfo=pytz.UTC)


def now_utc_timestamp() -> int:
    """
    Current seconds since UTC Unix epoch
    :return: UTC Unix timestamp
    """
    now = datetime.utcnow()
    return int((now - utc_epoch_datetime()).total_seconds())
