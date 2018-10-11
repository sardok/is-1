from flask import current_app, g, request, Blueprint, jsonify

from app.schedule_utils import query_by_names, query_by_user_type, schedule, intersect_interview_schedules
from app.services import UserType

api = Blueprint('schedule', __name__)


@api.route('/interviewer', methods=['POST'])
def schedule_interviewer():
    payload = request.get_json()
    scheduled = schedule(UserType.Interviewer, payload, g.interivew_calendar, current_app.logger)
    current_app.info('Create %d entries for %s', len(scheduled), payload['name'])


@api.route('/candidate', methods=['POST'])
def schedule_candidate():
    payload = request.get_json()
    scheduled = schedule(UserType.Candidate, payload, g.interview_calendar, current_app.logger)
    current_app.info('Create %d entries for %s', len(scheduled), payload['name'])


@api.route('/', method=['GET'])
def query():
    interviewers = request.args.getlist('interviewer')
    candidates = request.args.getlist('candidate')
    interviewers_schedules, candidates_schedules = query_by_names(interviewers, candidates, g.interview_calendar)
    res = intersect_interview_schedules(interviewers_schedules, candidates_schedules)
    return jsonify(res)


@api.route('/interviewers', method=['GET'])
def query_candidates():
    return query_by_user_type(UserType.Interviewer, g.interview_calendar)


@api.route('/candidates', method=['GET'])
def query_candidates():
    return query_by_user_type(UserType.Candidate, g.interview_calendar)


@api.route('/all', method=['GET'])
def query_all():
    return g.interviewer_calendar.query()
