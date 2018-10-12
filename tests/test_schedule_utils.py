from datetime import datetime
from app.services import InterviewSchedule, UserType
from app.schedule_utils import get_intersection_by_begin_dt, intersect_interview_schedules


def test_intersection_by_begin_1():
    data = [
        [
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 8), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 9), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 10), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 11), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 12), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 13), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 14), None)
        ],
        [
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 10), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 11), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 12), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 13), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 14), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 15), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 17), None),
        ],
        [
            InterviewSchedule('user_3', UserType.Candidate, datetime(2018, 10, 11, 14), None),
            InterviewSchedule('user_3', UserType.Candidate, datetime(2018, 10, 11, 15), None),
            InterviewSchedule('user_3', UserType.Candidate, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('user_3', UserType.Candidate, datetime(2018, 10, 11, 17), None),
        ]
    ]
    res = get_intersection_by_begin_dt(data)
    assert len(res) == 3
    assert [x.name for x in res] == ['user_1', 'user_2', 'user_3']


def test_intersection_by_begin_2():
    data = [
        [
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 10), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 11), None),
        ]
    ]
    res = get_intersection_by_begin_dt(data)
    assert len(res) == 2


def test_intersection_by_begin_3():
    data = [
        [
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 10), None),
            InterviewSchedule('user_1', UserType.Candidate, datetime(2018, 10, 11, 11), None),
        ],
        [
            InterviewSchedule('user_2', UserType.Candidate, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('user_2', UserType.Candidate, datetime(2018, 10, 11, 17), None),
        ]
    ]
    res = get_intersection_by_begin_dt(data)
    assert len(res) == 0


def test_intersection_by_begin_4():
    data = [
        [
            InterviewSchedule('user_1', UserType.Interviewer, datetime(2018, 10, 11, 11), None),
        ],
        [], []
    ]
    res = get_intersection_by_begin_dt(data)
    assert len(res) == 0


def test_intersect_interview_schedules_1():
    interviewers = [
        [
            InterviewSchedule('user_1', UserType.Interviewer, datetime(2018, 10, 11, 15), None),
            InterviewSchedule('user_1', UserType.Interviewer, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('user_1', UserType.Interviewer, datetime(2018, 10, 11, 17), None),
        ],
        [
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 17), None),
            InterviewSchedule('user_2', UserType.Interviewer, datetime(2018, 10, 11, 18), None),
        ]
    ]
    res = intersect_interview_schedules(interviewers, [])
    assert len(res) == 4
    assert [x['name'] for x in res] == ['user_1', 'user_1', 'user_2', 'user_2']


def test_intersect_interview_schedules_2():
    candidates = [
        [
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 13), None),
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 14), None),
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 15), None),
        ],
        [
            InterviewSchedule('candidate_2', UserType.Candidate, datetime(2018, 10, 11, 14), None),
            InterviewSchedule('candidate_2', UserType.Candidate, datetime(2018, 10, 11, 20), None),
        ]
    ]
    res = intersect_interview_schedules([], candidates)
    assert len(res) == 2
    assert res[0]['begin'] == datetime(2018, 10, 11, 14)


def test_intersect_interview_schedules_3():
    interviewers = [
        [
            InterviewSchedule('interviewer_1', UserType.Interviewer, datetime(2018, 10, 11, 14), None),
            InterviewSchedule('interviewer_1', UserType.Interviewer, datetime(2018, 10, 11, 15), None),
            InterviewSchedule('interviewer_1', UserType.Interviewer, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('interviewer_1', UserType.Interviewer, datetime(2018, 10, 11, 17), None),
        ],
        [
            InterviewSchedule('interviewer_2', UserType.Interviewer, datetime(2018, 10, 11, 16), None),
            InterviewSchedule('interviewer_2', UserType.Interviewer, datetime(2018, 10, 11, 17), None),
            InterviewSchedule('interviewer_2', UserType.Interviewer, datetime(2018, 10, 11, 18), None),
        ],
    ]
    candidates = [
        [
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 17), None),
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 18), None),
        ]
    ]
    res = intersect_interview_schedules(interviewers, candidates)
    assert len(res) == 3
    assert [x['name'] for x in res] == ['interviewer_1', 'interviewer_2', 'candidate_1']
    assert {x['begin'] for x in res} == {datetime(2018, 10, 11, 17)}


def test_intersect_interview_schedules_4():
    interviewers = [
        [
            InterviewSchedule('interviewer_1', UserType.Interviewer, datetime(2018, 10, 11, 11), None),
        ],
        [
            InterviewSchedule('interviewer_2', UserType.Interviewer, datetime(2018, 10, 11, 12), None),
        ]
    ]
    candidates = [
        [
            InterviewSchedule('candidate_1', UserType.Candidate, datetime(2018, 10, 11, 11), None),
        ],
        [
            InterviewSchedule('candidate_2', UserType.Candidate, datetime(2018, 10, 11, 20), None),
        ]
    ]
    res = intersect_interview_schedules(interviewers, candidates)
    assert len(res) == 0
