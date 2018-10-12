import operator
from flask import current_app, request, Blueprint, jsonify
from app.schedule_utils import query_by_names, query_by_user_type, query_all as query_all_
from app.schedule_utils import schedule, intersect_interview_schedules
from app.services import UserType
from app import get_interview_calendar

api = Blueprint('schedule', __name__)


@api.route('/interviewer', methods=['POST'])
def schedule_interviewer():
    payload = request.get_json()
    calendar = get_interview_calendar()
    scheduled = schedule(UserType.Interviewer, payload, calendar, current_app.logger)
    current_app.logger.info('Create %d entries for %s', len(scheduled), payload['name'])
    return jsonify(scheduled)


@api.route('/candidate', methods=['POST'])
def schedule_candidate():
    payload = request.get_json()
    calendar = get_interview_calendar()
    scheduled = schedule(UserType.Candidate, payload, calendar, current_app.logger)
    current_app.logger.info('Create %d entries for %s', len(scheduled), payload['name'])
    return jsonify(scheduled)


@api.route('/query', methods=['GET'])
def query():
    interviewers = request.args.getlist('interviewer')
    candidates = request.args.getlist('candidate')
    current_app.logger.info('Requested interviewers: %s, candidates: %s', interviewers, candidates)
    calendar = get_interview_calendar()
    interviewers_schedules, candidates_schedules = query_by_names(interviewers, candidates, calendar)
    schedules = intersect_interview_schedules(interviewers_schedules, candidates_schedules)
    return jsonify(sorted(schedules, key=operator.itemgetter('begin')))


@api.route('/interviewers', methods=['GET'])
def query_interviewers():
    calendar = get_interview_calendar()
    schedules = query_by_user_type(UserType.Interviewer, calendar)
    return jsonify(sorted(schedules, key=operator.itemgetter('begin')))


@api.route('/candidates', methods=['GET'])
def query_candidates():
    calendar = get_interview_calendar()
    schedules = query_by_user_type(UserType.Candidate, calendar)
    return jsonify(sorted(schedules, key=operator.itemgetter('begin')))


@api.route('/all', methods=['GET'])
def query_all():
    calendar = get_interview_calendar()
    schedules = query_all_(calendar)
    return jsonify(sorted(schedules, key=operator.itemgetter('begin')))
