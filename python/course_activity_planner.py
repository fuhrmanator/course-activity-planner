#!/usr/bin/env python3
import os
import uuid
import requests
import tarfile
import tempfile
import json
import jwt

from functools import wraps
from jwt import DecodeError, ExpiredSignature
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory, g
from models import Planning
from database import db_session, init_db, init_engine, clear_db

from interpreter import Interpreter, InvalidSyntaxException
from moodle import MoodleCourse
from ics_calendar import CalendarReader
from common import CAPException


app = Flask(__name__)


def login_req(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return jsonify(message='Please login'), 401
        try:
            payload = _parse_token_from_header(request)
            g.user_id = payload['sub']
            return f(*args, **kwargs)
        except DecodeError:
            return jsonify(message='Your session is invalid'), 401
        except ExpiredSignature:
            return jsonify(message='\
Your session has expired. Please login again.'), 401

    return decorated_func


@app.route('/api/me')
@login_req
def me():
    return jsonify({'user_id': g.user_id})


@app.route('/api/auth/google', methods=['POST'])
def auth_google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = '\
https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Exchange authorization code for access token
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Retrieve information about the current user from token
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    # create token from google unique user id
    token = _create_token(profile['sub'])
    return jsonify(token=token)


@app.route('/api/planning', methods=['POST'])
@login_req
def new_planning():
    user_id = g.user_id
    planning_id = _generate_planning_uuid()
    folder = os.path.join(app.config['UPLOAD_FOLDER'], planning_id)
    if os.path.isdir(folder):
        raise Exception('Planning uuid collision. UUID4 busted ?')
    os.makedirs(folder)

    # Get ICS
    if 'ics_url' in request.form:
        try:
            ics_url = request.form['ics_url']
            ics_fullpath = _dl_and_save_ics_file(ics_url, folder)
        except CAPException as e:
            return e.res
    elif 'ics_file' in request.files:
        ics_file = request.files['ics_file']
        ics_fullpath = _save_ics_file(ics_file, folder)
    else:
        return _bad_request()

    # Get MBZ or empty mbz_fullpath
    mbz_fullpath = None
    if 'mbz_file' in request.files:
        mbz_file = request.files['mbz_file']
        mbz_fullpath = _save_mbz_file(mbz_file, folder)

    # .get() returns None if key is not defined
    # Client should be pressured to send the information from the front-end
    name = request.form.get('name')
    year = request.form.get('year')
    semester = request.form.get('semester')
    group = request.form.get('group')

    planning = Planning(planning_id, user_id, '', ics_fullpath, mbz_fullpath,
                        name, year, semester, group)
    db_session.add(planning)
    db_session.commit()

    return jsonify(planning=planning.as_pub_dict())


@app.route('/api/planning/<uuid>', methods=['PUT'])
@login_req
def update_planning(uuid):
    req = request.get_json()

    if not req or 'planning' not in req:
        return _bad_request()

    try:
        planning = _get_planning(uuid, g.user_id)
    except CAPException as e:
        return e.res

    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404

    planning.planning_txt = req['planning']

    db_session.add(planning)
    db_session.commit()

    return jsonify({}), 200


@app.route('/api/planning/', methods=['GET'])
@login_req
def get_all_plannings_for_user():
    try:
        plannings = _get_plannings_for_user(g.user_id)
    except CAPException as e:
        return e.res

    pub = map(lambda planning: planning.as_pub_dict(), plannings)
    return jsonify({'plannings': list(pub)}), 200


@app.route('/api/planning/<uuid>', methods=['GET'])
@login_req
def get_planning(uuid):
    try:
        planning = _get_planning(uuid, g.user_id)
    except CAPException as e:
        return e.res
    return jsonify({'planning': planning.as_pub_dict()})


@app.route('/api/planning/<uuid>', methods=['DELETE'])
@login_req
def delete_planning(uuid):
    try:
        planning = _get_planning(uuid, g.user_id)
        db_session.delete(planning)
        db_session.commit()
    except CAPException as e:
        return e.res
    return jsonify({}), 204


@app.route('/api/planning/<uuid>/preview', methods=['GET'])
@login_req
def preview_planning(uuid):
    try:
        planning = _get_planning(uuid, g.user_id)
    except CAPException as e:
        return e.res
    moodle_archive_path = planning.mbz_fullpath
    planning_txt = planning.planning_txt

    # Make tmp directory for MBZ extraction
    with tempfile.TemporaryDirectory() as tmp_path:
        try:
            calendar = CalendarReader(planning.ics_fullpath)
            calendar_meetings = calendar.get_all_meetings()
        except Exception as e:
            _bad_cal()

        # Extract Moodle course to tmp folder
        course = None
        if moodle_archive_path:
            try:
                with tarfile.open(moodle_archive_path) as tar_file:
                    tar_file.extractall(tmp_path)
                    course = MoodleCourse(tmp_path)
            except Exception as e:
                return jsonify(
                    alerts=[{'type': 'danger',
                            'msg': 'MBZ file could not be read.'}]), 400

    alerts = []
    preview = None
    inventory = None
    try:
        interpreter = Interpreter(calendar_meetings, course)
        inventory = _build_inventory(interpreter, planning_txt)
        preview = _build_preview(interpreter, planning_txt)
        alerts = _build_alerts_for_preview(interpreter)
    except InvalidSyntaxException as e:
        alerts.append({'type': 'danger', 'msg': e.message})
    return jsonify(
        {'preview': preview, 'inventory': inventory, 'alerts': alerts}), 200


@app.route('/api/planning/<uuid>/mbz', methods=['GET'])
@login_req
def download_planning(uuid):
    try:
        planning = _get_planning(uuid, g.user_id)
    except CAPException as e:
        return e.res

    moodle_archive_path = planning.mbz_fullpath
    planning_txt = planning.planning_txt

    if not planning_txt:
        return _bad_request()

    # Make tmp directory for MBZ extraction and ics download
    with tempfile.TemporaryDirectory() as tmp_path:
        # Download calendar to tmp folder
        calendar = CalendarReader(planning.ics_fullpath)
        calendar_meetings = calendar.get_all_meetings()

        # Extract Moodle course to tmp folder
        with tarfile.open(moodle_archive_path) as tar_file:
            tar_file.extractall(tmp_path)
            course = MoodleCourse(tmp_path)

        interpreter = Interpreter(calendar_meetings, course)
        for line in planning_txt.split('\n'):
            event = interpreter.get_new_event_from_string(line)
            course.replace_event(event)

        folder = os.path.join(app.config['UPLOAD_FOLDER'], uuid)
        latest_mbz_path = os.path.join(folder, 'latest.mbz')

        course.write(latest_mbz_path)
        return send_from_directory(
            folder, 'latest.mbz', as_attachment=True)


@app.route('/')
def index():
    return send_from_directory('../public', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    if '.' not in path:
        return index()

    return send_from_directory('../public', path)


def _create_token(id):
    payload = {
        'sub': id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def _parse_token_from_header(req):
    # Bearer <token>
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


def _generate_planning_uuid():
    return str(uuid.uuid4())


def _has_planning(uuid):
    return Planning.query.filter(Planning.uuid == uuid).count() > 0


def __get_planning(uuid):
    """Get planning from uuid bypassing user id check"""
    return Planning.query.filter(Planning.uuid == uuid).first()


def _get_planning(uuid, user_id):
    """Get planning from uuid and user id"""
    planning = __get_planning(uuid)
    if not planning:
        _planning_not_found(uuid)
    if planning.user_id != str(user_id):
        _forbidden()
    return planning


def _get_plannings_for_user(user_id):
    """Get all plannings from user id"""
    return Planning.query.filter(Planning.user_id == user_id).all()


def _get_planning_bypass(uuid):
    return __get_planning(uuid)


def _save_ics_file(ics_file, folder):
    ics_fullpath = os.path.join(folder, 'original_calendar.ics')
    ics_file.save(ics_fullpath)
    return ics_fullpath


def _save_mbz_file(mbz_file, folder):
    mbz_fullpath = os.path.join(folder, 'original_archive.mbz')
    mbz_file.save(mbz_fullpath)
    return mbz_fullpath


def _dl_and_save_ics_file(ics_url, folder):
    try:
        ics_fullpath = os.path.join(folder, 'original_calendar.ics')
        r = requests.get(ics_url, stream=True)

        with open(ics_fullpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
    except Exception:
        _bad_cal()
    return ics_fullpath


def _build_inventory(interpreter, planning_txt):
    inventory = {'meetings': [], 'activities': []}
    calendar_meetings = interpreter.meetings
    moodle_activities = interpreter.course.activities \
        if interpreter.course else []

    for meeting_type in calendar_meetings:
        for i, meeting in enumerate(calendar_meetings[meeting_type]):
            rel_id = i + 1
            inventory['meetings'].append({
                'rel_id': rel_id,
                'key_str': meeting.get_key(),
                'title': meeting.get_title()})

    for activity_type in moodle_activities:
        for i, activity in enumerate(moodle_activities[activity_type]):
            rel_id = i + 1
            inventory['activities'].append({
                'rel_id': rel_id,
                'key_str': activity.get_key(),
                'title': activity.get_title()})
    return inventory


def _get_preview_items_for_planning(interpreter, planning_txt):
    preview = []

    if planning_txt:
        for line in planning_txt.split('\n'):
            activity = interpreter.get_new_event_from_string(line)
            activity_pretty_name = activity.get_pretty_name()

            for i, event_pretty_name, in enumerate(activity.event_pretty_names):
                timestamp = activity.get_timestamp_at_index(i)

                if timestamp == 0:
                    continue
                preview.append({
                    'title': '%s %d %s' % (
                        activity_pretty_name, activity.rel_id,
                        event_pretty_name),
                    'key_str': activity.get_key(),
                    'timestamp': timestamp})
    return preview


def _add_preview_items_for_calendar(calendar_meetings, preview_items):
    for meeting_type in calendar_meetings:
        clazz = meeting_type.__name__

        for i, meeting in enumerate(calendar_meetings[meeting_type]):
            rel_id = i + 1
            preview_items.append({
                'title': '%s %d opens' % (clazz, rel_id),
                'key_str': meeting.get_key(),
                'timestamp': meeting.get_start_timestamp()})
            preview_items.append({
                'title': '%s %d closes' % (clazz, rel_id),
                'key_str': meeting.get_key(),
                'timestamp': meeting.get_end_timestamp()})
    return preview_items


def _build_preview(interpreter, planning_txt):
    preview = _get_preview_items_for_planning(interpreter, planning_txt)

    calendar_meetings = interpreter.meetings
    preview = _add_preview_items_for_calendar(calendar_meetings, preview)

    # Return preview sorted by timestamp
    return sorted(preview, key=lambda p: p['timestamp'])


def _build_alerts_for_preview(interpreter):
    alerts = []
    moodle_activities = interpreter.course.activities \
        if interpreter.course else []
    for activity_type in moodle_activities:
        for activity in moodle_activities[activity_type]:
            if activity.get_start_datetime() > activity.get_end_datetime():
                alerts.append(
                    {'type': 'warning',
                     'msg': '%s %d ends before it starts.' %
                     (activity.get_pretty_name(), activity.rel_id)})
    return alerts


def _bad_request():
    return jsonify({'message': 'Bad request.'}), 400


def _forbidden():
    """Raiser function"""
    raise CAPException(
        {'type': 'danger',
         'msg': 'You are not allowed to view this ressource.'}, 403)


def _planning_not_found(uuid):
    """Raiser function"""
    raise CAPException(
        {'type': 'danger',
         'msg': 'Planning with uuid "%s" not found' % uuid}, 404)


def _bad_cal():
    """Raiser function"""
    raise CAPException(
        {'type': 'danger',
         'msg': 'Calendar file is not a valid ICS file.'}, 400)


def _clear_db():
    db_session.rollback()
    clear_db()


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)
    app.config.from_pyfile('config/%s_secret.py' % env, silent=True)

    init_engine(app.config['DATABASE_URI'])
    init_db()

    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
