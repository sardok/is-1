from typing import Tuple, Optional
from datetime import datetime
from app.services import data
from app.services.user_type import UserType
from app.services.model import InterviewSchedule
from app.services.utils import iter_time_frame


class InterviewCalendar:
    def __init__(self, interview_duration=1):
        self.delta = interview_duration

    def iter_time_frame(self, time_frame: Tuple[datetime, datetime]):
        return iter_time_frame(time_frame, self.delta)

    def allocate(self, name: str, user_type: UserType, time_frame: Tuple[datetime, datetime]):
        allocated = []
        for dt in self.iter_time_frame(time_frame):
            schedule_data = data.create_schedule(name, user_type.value, dt, self.delta)
            schedule = InterviewSchedule.from_data(schedule_data)
            allocated.append(schedule)
        return allocated

    def deallocate(self, name: str, user_type: UserType, time_frame: Tuple[datetime, datetime]):
        begins = [dt for dt in self.iter_time_frame(time_frame)]
        data.delete_schedules([name], [user_type.value], begins)

    def query(self, name: Optional[str]=None, user_type: Optional[UserType]=None,
              time_frame: Optional[Tuple[datetime, datetime]]=None):
        names = [name] if name else []
        types = [user_type.value] if user_type else []
        begins = [dt for dt in self.iter_time_frame(time_frame)] if time_frame else []
        for schedule_data in data.query_schedules(names, types, begins):
            yield InterviewSchedule.from_data(schedule_data)
