from typing import Tuple
from dateutil import parser as dt_parser
from app.types import TimeFrameType


def parse_schedule_data(schedule: Tuple[str, str]) -> TimeFrameType:
    return tuple(map(dt_parser.parse, schedule))
