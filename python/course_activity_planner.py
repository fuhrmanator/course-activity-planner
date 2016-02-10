#!/usr/bin/env python3
import os
import uuid
import requests
import tarfile
import tempfile

from flask import Flask, jsonify, request, send_from_directory
from models import Planning
from database import db_session, init_db, init_engine, clear_db

from interpreter import Interpreter
from moodle import MoodleCourse
from ics_calendar import CalendarReader


app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def new_planning():
    ics_url = request.form['ics_url']
    if not ics_url:
        return _bad_request()

    mbz_file = request.files['file']
    if not mbz_file:
        return _bad_request()

    planning_id = _generate_planning_uuid()

    folder = os.path.join(app.config['UPLOAD_FOLDER'], planning_id)
    if os.path.isdir(folder):
        raise Exception('Planning uuid collision. UUID4 busted ?')
    os.makedirs(folder)

    mbz_fullpath = _save_mbz_file(mbz_file, folder)

    planning = Planning(planning_id, '', ics_url, mbz_fullpath)
    db_session.add(planning)
    db_session.commit()

    return jsonify(planning=planning.as_pub_dict())


@app.route('/api/planning/<uuid>', methods=['PUT'])
def update_planning(uuid):
    req = request.get_json()

    if not req or 'planning' not in req:
        return _bad_request()

    planning = _get_planning(uuid)

    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404

    planning.planning_txt = req['planning']

    db_session.add(planning)
    db_session.commit()

    return jsonify({}), 200


@app.route('/api/planning/<uuid>/', methods=['GET'])
def get_planning(uuid):
    planning = _get_planning(uuid)
    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404
    return jsonify({'planning': planning.as_pub_dict()})


def _build_inventory(interpreter, planning_txt):
    inventory = []
    calendar_meetings = interpreter.meetings
    moodle_activities = interpreter.course.activities

    for meeting_type in calendar_meetings:
        for i, meeting in enumerate(calendar_meetings[meeting_type]):
            rel_id = i + 1
            inventory.append({
                'key': '%s%d' % (meeting.get_key(), rel_id),
                'title': meeting.get_title()})

    for activity_type in moodle_activities:
        for i, activity in enumerate(moodle_activities[activity_type]):
            rel_id = i + 1
            inventory.append({
                'key': '%s%d' % (activity.get_key(), rel_id),
                'title': activity.get_title()})
    return inventory


def _build_preview(interpreter, planning_txt):
    # Build preview
    preview = []
    calendar_meetings = interpreter.meetings

    if planning_txt:
        for line in planning_txt.split('\n'):
            event = interpreter.get_new_event_from_string(line)
            pretty_event_name = event.get_pretty_name()

            preview.append({
                'title': '%s %d opens' % (pretty_event_name, event.rel_id),
                'timestamp': event.get_start_timestamp()})
            preview.append({
                'title': '%s %d closes' % (pretty_event_name, event.rel_id),
                'timestamp': event.get_end_timestamp()})

    for meeting_type in calendar_meetings:
        clazz = meeting_type.__name__

        for i, meeting in enumerate(calendar_meetings[meeting_type]):
            rel_id = i + 1
            preview.append({
                'title': '%s %d opens' % (clazz, rel_id),
                'timestamp': meeting.get_start_timestamp()})
            preview.append({
                'title': '%s %d closes' % (clazz, rel_id),
                'timestamp': meeting.get_end_timestamp()})

    # Return preview sorted by timestamp
    return sorted(preview, key=lambda p: p['timestamp'])


@app.route('/api/planning/<uuid>/preview', methods=['GET'])
def preview_planning(uuid):
    planning = _get_planning(uuid)
    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404

    moodle_archive_path = planning.mbz_fullpath
    planning_txt = planning.planning_txt

    # Make tmp directory for MBZ extraction and ics download
    with tempfile.TemporaryDirectory() as tmp_path:
        # Download calendar to tmp folder
        calendar_path = _dl_and_save_ics_file(planning.ics_url, tmp_path)
        calendar = CalendarReader(calendar_path)
        calendar_meetings = calendar.get_all_meetings()

        # Extract Moodle course to tmp folder
        with tarfile.open(moodle_archive_path) as tar_file:
            tar_file.extractall(tmp_path)
            course = MoodleCourse(tmp_path)

    interpreter = Interpreter(calendar_meetings, course)
    preview = _build_preview(interpreter, planning_txt)
    inventory = _build_inventory(interpreter, planning_txt)

    return jsonify({'preview': preview, 'inventory': inventory}), 200


@app.route('/api/planning/<uuid>/mbz', methods=['GET'])
def download_planning(uuid):
    planning = _get_planning(uuid)
    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404

    moodle_archive_path = planning.mbz_fullpath
    planning_txt = planning.planning_txt

    if not planning_txt:
        return _bad_request()

    # Make tmp directory for MBZ extraction and ics download
    with tempfile.TemporaryDirectory() as tmp_path:
        # Download calendar to tmp folder
        calendar_path = _dl_and_save_ics_file(planning.ics_url, tmp_path)
        calendar = CalendarReader(calendar_path)
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


def _generate_planning_uuid():
    return str(uuid.uuid4())


def _has_planning(uuid):
    return Planning.query.filter(Planning.uuid == uuid).count() > 0


def _get_planning(uuid):
    return Planning.query.filter(Planning.uuid == uuid).first()


def _save_mbz_file(mbz_file, folder):
    mbz_fullpath = os.path.join(folder, 'original_archive.mbz')
    mbz_file.save(mbz_fullpath)
    return mbz_fullpath


def _dl_and_save_ics_file(ics_url, folder):
    ics_fullpath = os.path.join(folder, 'original_calendar.ics')
    r = requests.get(ics_url, stream=True)

    with open(ics_fullpath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
    return ics_fullpath


def _bad_request():
    return jsonify({'message': 'Bad request.'}), 400


def _clear_db():
    db_session.rollback()
    clear_db()


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)

    init_engine(app.config['DATABASE_URI'])
    init_db()

    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
