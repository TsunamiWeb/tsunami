from dateutil import parser, tz
import datetime


_tzinfo = tz.gettz('Asia/Shanghai')


def to_str(datetime, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(format)


def cst(datetime, format='%Y-%m-%d %H:%M'):
    return datetime.astimezone(_tzinfo).strftime(format)


def utc(datetime, format='%Y-%m-%d %H:%M:%S%z'):
    return datetime.astimezone(tz.gettz('UTC')).strftime(format)


def now(_tz=tz.gettz('UTC')):
    return datetime.datetime.utcnow().replace(
        tzinfo=tz.gettz('UTC')).astimezone(_tz)


def today(_tz=tz.gettz('Asia/Shanghai')):
    _today = now(_tz=_tz)
    return datetime.datetime(
        _today.year, _today.month,
        _today.day, tzinfo=_tz)
