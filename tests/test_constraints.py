import pytest
from datetime import datetime, timedelta
from app import constraints


def test_time_frame_sanity():
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    time_frame = (tomorrow, now)
    with pytest.raises(RuntimeError):
        constraints.time_frame_sanity(time_frame)


def test_time_frame_hour_1():
    begin = datetime(2018, 10, 10, 12, 30)
    end = datetime(2018, 10, 10, 13)
    time_frame = (begin, end)
    with pytest.raises(RuntimeError):
        constraints.time_frame_hour(time_frame)


def test_time_frame_hour_2():
    begin = datetime(2018, 10, 10, 12)
    end = datetime(2018, 10, 10, 13, 30)
    time_frame = (end, begin)
    with pytest.raises(RuntimeError):
        constraints.time_frame_hour(time_frame)


def test_time_frame_hour_3():
    begin = datetime(2018, 10, 10, 12, 30)
    end = datetime(2018, 10, 10, 13, 30)
    time_frame = (begin, end)
    with pytest.raises(RuntimeError):
        constraints.time_frame_hour(time_frame)


def test_time_frame_weekday_1():
    begin = datetime(2018, 10, 10, 13)
    end = datetime(2018, 10, 13)
    time_frame = (begin, end)
    with pytest.raises(RuntimeError):
        constraints.time_frame_weekdays(time_frame)


def test_time_frame_weekday_2():
    begin = datetime(2018, 10, 7, 12)
    end = datetime(2018, 10, 10)
    time_frame = (begin, end)
    with pytest.raises(RuntimeError):
        constraints.time_frame_weekdays(time_frame)


def test_time_frame_weekday_3():
    begin = datetime(2018, 10, 7, 12)
    end = datetime(2018, 10, 13)
    time_frame = (begin, end)
    with pytest.raises(RuntimeError):
        constraints.time_frame_weekdays(time_frame)


def test_long_name():
    name = 'a' * 255
    with pytest.raises(RuntimeError):
        constraints.long_name(name)
