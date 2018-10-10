import pytest
from datetime import datetime, timedelta
from app import services


@pytest.fixture()
def db_connection():
    services.set_test_mode(True)
    services.database_init('sqlite:///:memory:')


@pytest.fixture()
def calendar(db_connection):
    return services.InterviewCalendar()


@pytest.fixture()
def test_data_set_1(calendar):
    user1_begin = datetime(2018, 7, 10, 8)
    user1_end = datetime(2018, 7, 10, 16)
    calendar.allocate('User 1', services.UserType.Interviewer, (user1_begin, user1_end))

    user2_begin = datetime(2018, 7, 10, 13)
    user2_end = datetime(2018, 7, 10, 17)
    calendar.allocate('User 2', services.UserType.Candidate, (user2_begin, user2_end))


def test_allocate_1(calendar: services.InterviewCalendar):
    begin = datetime(2018, 7, 10, 13)
    end = datetime(2018, 7, 10, 15)
    allocated = calendar.allocate('User 1', services.UserType.Candidate, (begin, end))

    assert len(allocated) == 2
    mid = begin + timedelta(hours=1)
    assert allocated[0] == services.InterviewSchedule('User 1', services.UserType.Candidate, begin, mid)
    assert allocated[1] == services.InterviewSchedule('User 1', services.UserType.Candidate, mid, end)


def test_query_1(calendar: services.InterviewCalendar, test_data_set_1):
    all_ = list(calendar.query())
    assert len(all_) == 12


def test_query_by_user_type_1(calendar: services.InterviewCalendar, test_data_set_1):
    interviews = list(calendar.query(user_type=services.UserType.Interviewer))
    assert len(interviews) == 8

    candidates = list(calendar.query(user_type=services.UserType.Candidate))
    assert len(candidates) == 4


def test_query_by_time_frame_1(calendar: services.InterviewCalendar, test_data_set_1):
    # This is available for interviewer only
    time_frame = (datetime(2018, 7, 10, 10), datetime(2018, 7, 10, 13))
    results = list(calendar.query(time_frame=time_frame))
    assert len(results) == 3


def test_query_by_time_frame_2(calendar: services.InterviewCalendar, test_data_set_1):
    # This is available for candidate only
    time_frame = (datetime(2018, 7, 10, 16), datetime(2018, 7, 10, 20))
    results = list(calendar.query(time_frame=time_frame))
    assert len(results) == 1


def test_query_by_time_frame_3(calendar: services.InterviewCalendar, test_data_set_1):
    # This is intersection time frame for both type of users
    time_frame = (datetime(2018, 7, 10, 13), datetime(2018, 7, 10, 16))
    results = list(calendar.query(time_frame=time_frame))
    assert len(results) == 3 * 2


def test_query_by_name_1(calendar: services.InterviewCalendar, test_data_set_1):
    results = list(calendar.query('User 1'))
    assert len(results) == 8


def test_query_by_name_2(calendar: services.InterviewCalendar, test_data_set_1):
    results = list(calendar.query('User 2'))
    assert len(results) == 4


def test_deallocate_valid_1(calendar: services.InterviewCalendar, test_data_set_1):
    # Remove valid time frame from User 1
    time_frame = (datetime(2018, 7, 10, 12), datetime(2018, 7, 10, 16))
    calendar.deallocate('User 1', services.UserType.Interviewer, time_frame)
    results = list(calendar.query('User 1'))
    assert len(results) == 4


def test_deallocate_valid_2(calendar: services.InterviewCalendar, test_data_set_1):
    time_frame = (datetime(2018, 7, 10, 13), datetime(2018, 7, 10, 17))
    calendar.deallocate('User 2', services.UserType.Candidate, time_frame)
    results = list(calendar.query('User 2'))
    assert len(results) == 0


def test_deallocate_invalid_1(calendar: services.InterviewCalendar, test_data_set_1):
    # Remove valid user with invalid time frame
    time_frame = (datetime(2018, 7, 11), datetime(2018, 7, 12))
    calendar.deallocate('User 1', services.UserType.Interviewer, time_frame)
    results = list(calendar.query('User 1'))
    assert len(results) == 8


def test_deallocate_invalid_2(calendar: services.InterviewCalendar, test_data_set_1):
    # Remove valid user with invalid type
    time_frame = (datetime(2018, 7, 10), datetime(2018, 7, 11))
    calendar.deallocate('User 1', services.UserType.Candidate, time_frame)
    results = list(calendar.query('User 1'))
    assert len(results) == 8


def test_deallocate_invalid_3(calendar: services.InterviewCalendar, test_data_set_1):
    # Remove invalid user
    time_frame = (datetime(2018, 7, 10), datetime(2018, 7, 11))
    calendar.deallocate('User 3', services.UserType.Interviewer, time_frame)
    results = list(calendar.query())
    assert len(results) == 12
