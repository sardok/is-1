from datetime import datetime
from typing import Tuple, Callable

TimeFrameType = Tuple[datetime, datetime]
NameConstraintType = Callable[[str], None]
TimeConstraintType = Callable[[TimeFrameType], None]
