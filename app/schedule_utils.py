import functools
from typing import List
from app.services import UserType
from app.utils import parse_schedule_data
from app.services import InterviewSchedule


def get_intersection_by_begin_dt(xss: List[List[InterviewSchedule]]):
    sets_of_datetimes = [{x.begin for x in xs} for xs in xss]
    intersected_datetimes = functools.reduce(lambda acc, x: acc & x, sets_of_datetimes)

    return [x for xs in xss for x in xs if x.begin in intersected_datetimes]


def query_by_names(interviewers, candidates, interview_calendar):
    """
    Executes query by given interviewer and/or candidate names.
    Returns intersection by schedule times.
    """
    interviewers_schedules = [list(interview_calendar.query(interviewer, UserType.Interviewer))
                              for interviewer in interviewers]
    candidates_schedules = [list(interview_calendar.query(candidate, UserType.Candidate))
                            for candidate in candidates]
    return interviewers_schedules, candidates_schedules


def to_serializable(f):
    @functools.wraps(f)
    def inner(*a, **kw):
        xs = f(*a, **kw)
        return [x.as_dict() for x in xs]
    return inner


@to_serializable
def intersect_interview_schedules(
        interviewers_schedules: List[List[InterviewSchedule]],
        candidates_schedules: List[List[InterviewSchedule]]):

    interviewer_intersections = get_intersection_by_begin_dt(interviewers_schedules) if interviewers_schedules else []
    candidate_intersections = get_intersection_by_begin_dt(candidates_schedules) if candidates_schedules else []
    if interviewers_schedules and candidates_schedules:
        return get_intersection_by_begin_dt([interviewer_intersections, candidate_intersections])
    else:
        return interviewer_intersections or candidate_intersections


@to_serializable
def query_by_user_type(user_type: UserType, interview_calendar):
    return interview_calendar.query(user_type=user_type)


@to_serializable
def query_all(interview_calendar):
    return interview_calendar.query()


@to_serializable
def schedule(user_type, payload, interview_calendar, logger):
    name = payload['name']
    schedules = payload.get('schedules', [])
    ret = []

    for schedule in schedules:
        try:
            time_frame = parse_schedule_data(schedule[:2])
            allocated = interview_calendar.allocate(name, user_type, time_frame)
            ret.extend(allocated)
        except:
            logger.error('Invalid schedule %s (name: %s)', schedule, name)
            raise

    return ret
