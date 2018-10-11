from flask import Flask, g
from app.services import database_init
from app.services import InterviewCalendar
from app import constraints


def create_interview_calendar():
    name_constraints = [constraints.long_name]
    time_frame_constraints = [
        constraints.time_frame_sanity,
        constraints.time_frame_weekdays,
        constraints.time_frame_hour]

    return InterviewCalendar(
        name_constraints=name_constraints,
        time_frame_constraints=time_frame_constraints)


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings')
    database_init(app.config['DB_URI'])

    from app.handlers import schedule
    app.register_blueprint(schedule.api, url_prefix='/schedule')

    with app.app_context():
        g.interview_calendar = create_interview_calendar()
    return app
