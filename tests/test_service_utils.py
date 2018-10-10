from datetime import datetime
from app.services.utils import iter_time_frame


def test_1():
    time_frame = (datetime(2018, 10, 8, 10), datetime(2018, 10, 8, 17))
    results = list(iter_time_frame(time_frame, 1))
    assert len(results) == 7
    for hour, result in zip(range(10, 20), results):
        expected = datetime(2018, 10, 8, hour)
        assert expected == result


def test_2():
    time_frame = (datetime(2018, 10, 8), datetime(2018, 10, 9))
    results = list(iter_time_frame(time_frame, 1))
    assert len(results) == 24

    expected_last = datetime(2018, 10, 8, 23)
    assert expected_last == results[-1]


def test_3():
    time_frame = (datetime(2018, 10, 8), datetime(2018, 10, 8))
    results = list(iter_time_frame(time_frame, 1))
    assert len(results) == 0
