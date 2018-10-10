from datetime import timedelta
from collections import namedtuple
from app.services.user_type import UserType


_InterviewSchedule = namedtuple('InterviewSchedule', ['name', 'type', 'begin', 'end'])


class InterviewSchedule(_InterviewSchedule):
    @classmethod
    def from_data(cls, data: dict):
        user_type = UserType(data['type'])
        begin = data['begin']
        end = begin + timedelta(hours=data['duration'])
        return cls(data['name'], user_type, begin, end)
