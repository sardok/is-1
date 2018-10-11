from datetime import datetime
from app.types import TimeFrameType


def long_name(name: str):
    if len(name) > 100:
        raise RuntimeError('Given name is too long.')


def time_frame_hour(time_frame: TimeFrameType):
    def is_good_dt(dt: datetime):
        return dt.minute == 0
    if not all([is_good_dt(x) for x in time_frame]):
        raise RuntimeError('Beginning of hours only allowed for scheduling.')


def time_frame_weekdays(time_frame: TimeFrameType):
    def is_good_day(dt: datetime):
        return 1 >= dt.isoweekday() <= 5

    if not all([is_good_day(x) for x in time_frame]):
        raise RuntimeError('Only weekdays are allowed for scheduling.')


def time_frame_sanity(time_frame: TimeFrameType):
    begin, end = time_frame
    if end <= begin:
        raise RuntimeError('Invalid Begin or End date.')
