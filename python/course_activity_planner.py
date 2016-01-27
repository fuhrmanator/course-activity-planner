#!/usr/bin/env python3
import os
import uuid
import json
import shutil
import requests
import tarfile
import tempfile

from flask import Flask, jsonify, request
from models import Planning
from database import db_session, init_db, init_engine, clear_db

from interpreter import Interpreter
from moodle import MoodleCourse
from ics_calendar import CalendarReader, Seminar, Practica


app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def new_planning():
    req = json.loads(request.form['data'])
    if not req or 'ics_url' not in req:
        return _bad_request()

    mbz_file = request.files['file']
    if not mbz_file:
        return _bad_request()

    ics_url = req['ics_url']

    planning_id = _generate_planning_uuid()

    folder = os.path.join(app.config['UPLOAD_FOLDER'], planning_id)
    if os.path.isdir(folder):
        raise Exception('Planning uuid collision. UUID4 busted ?')
    os.makedirs(folder)

    mbz_fullpath = _save_mbz_file(mbz_file, folder)
    ics_fullpath = _dl_and_save_ics_file(ics_url, folder)

    planning = Planning(planning_id, '', ics_fullpath, mbz_fullpath)
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


@app.route('/api/planning/<uuid>/preview', methods=['GET'])
def preview_planning(uuid):
    planning = _get_planning(uuid)
    if not planning:
        return jsonify(
            {'message': 'Planning with uuid "%s" not found' % uuid}), 404
    calendar_path = planning.ics_fullpath
    moodle_archive_path = planning.mbz_fullpath
    planning_txt = planning.planning_txt

    # Read calendar
    calendar = CalendarReader(calendar_path)
    calendar_meetings = calendar.get_all_meetings()

    # Read Moodle course
    tmp_path = tempfile.mkdtemp()
    with tarfile.open(moodle_archive_path) as tar_file:
        tar_file.extractall(tmp_path)
        course = MoodleCourse(tmp_path)
        shutil.rmtree(tmp_path)

    interpreter = Interpreter(calendar_meetings, course)
    # TODO read multiple lines
    event = interpreter.get_new_event_from_string(planning_txt)

    preview = []
    preview.append({
        'title': "Quiz 1 opens",
        'timestamp': event.get_start_timestamp()})
    preview.append({
        'title': "Quiz 1 closes",
        'timestamp': event.get_end_timestamp()})

    return jsonify({'preview': preview}), 200


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
