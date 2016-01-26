#!/usr/bin/env python3
import os
import uuid
import json
import requests

from flask import Flask, jsonify, request
from models import Planning
from database import db_session, init_db, init_engine

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def new_planning():
    req = json.loads(request.form['data'])
    if not req or 'ics_url' not in req or 'planning' not in req:
        return _bad_request()

    mbz_file = request.files['file']
    if not mbz_file:
        return _bad_request()

    ics_url = req['ics_url']
    planning_txt = req['planning']

    planning_id = _generate_planning_uuid()

    folder = os.path.join(app.config['UPLOAD_FOLDER'], planning_id)
    if os.path.isdir(folder):
        raise Exception('Planning id collision. UUID4 busted ?')
    os.makedirs(folder)

    mbz_fullpath = _save_mbz_file(mbz_file, folder)
    ics_fullpath = _dl_and_save_ics_file(ics_url, folder)

    planning = Planning(planning_id, planning_txt,
                        ics_fullpath, mbz_fullpath)
    db_session.add(planning)
    db_session.commit()

    return jsonify(planning=planning.as_pub_dict())


def _has_planning(uuid):
    pass


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


def _generate_planning_uuid():
    return str(uuid.uuid4())


def _bad_request():
    return jsonify({'message': 'Bad request.'}), 400


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)

    init_engine(app.config['DATABASE_URI'])
    init_db()

    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
