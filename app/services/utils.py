from datetime import datetime, timedelta
from typing import Tuple


def iter_time_frame(time_frame: Tuple[datetime, datetime], delta_hours):
    begin, end = time_frame
    while begin < end:
        yield begin
        begin += timedelta(hours=delta_hours)
