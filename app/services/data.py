import logging
from typing import List
from contextlib import contextmanager
from datetime import datetime
from peewee import Model, Proxy
from peewee import CharField, IntegerField, DateTimeField
from playhouse.shortcuts import model_to_dict
from playhouse.db_url import connect as db_connect

database = Proxy()
logger = logging.getLogger(__name__)
_test_mode = False


class _Base(Model):
    class Meta:
        database = database

    def as_dict(self):
        return model_to_dict(self)


class Schedule(_Base):
    name = CharField()
    type = IntegerField()
    begin = DateTimeField()
    duration = IntegerField(default=1)


@contextmanager
def database_connection_context():
    global _test_mode
    if _test_mode:
        yield database
    else:
        with database.connection_context() as db:
            yield db


def get_query_predicates(names: List[str], types: List[int], begins: List[datetime]):
    predicates = []

    if names:
        predicates.append((Schedule.name << names))

    if types:
        predicates.append((Schedule.type << types))

    if begins:
        predicates.append((Schedule.begin << begins))

    return predicates


def query_schedules(names: List[str], types: List[int], begins: List[datetime]) -> List[Schedule]:
    with database_connection_context():
        predicates = get_query_predicates(names, types, begins)
        schedules = (Schedule
                     .select()
                     .where(*(predicates or [None]))
                     .order_by(Schedule.id.desc())
                     .execute())
        return [schedule.as_dict() for schedule in schedules]


def create_schedule(name: str, user_type: int, begin: datetime, duration: int) -> Schedule:
    with database_connection_context():
        schedule, _ = Schedule.get_or_create(
            name=name, type=user_type, begin=begin, duration=duration)
        return schedule.as_dict()


def delete_schedules(names: List[str], types: List[int], begins: List[datetime]):
    with database_connection_context():
        predicates = get_query_predicates(names, types, begins)
        if not predicates:
            logger.warning('Deleting all schedules!')

        Schedule.delete().where(*(predicates or [None])).execute()


def is_db_initialized():
    return database.obj is not None


def set_test_mode(mode):
    global _test_mode
    _test_mode = mode
    if is_db_initialized():
        logger.warning('Database is initialized before setting test mode!')


def init(uri):
    _database = db_connect(uri)
    database.initialize(_database)
    database.create_tables([Schedule], safe=True)
    if not _test_mode:
        database.close()
