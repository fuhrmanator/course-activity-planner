#!/usr/bin/env python3
import os
import uuid
import json
import requests

from flask import Flask, session, jsonify, request

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def post_planning():
    req = json.loads(request.form['data'])
    if not req or 'ics_url' not in req or 'planning' not in req:
        return _bad_request()

    mbz_file = request.files['file']
    if not mbz_file:
        return _bad_request()

    ics_url = req['ics_url']

    transaction_id = _generate_transaction_uuid()
    session['transaction_id'] = transaction_id

    _save_mbz_file(mbz_file, transaction_id)
    _dl_and_save_ics_file(ics_url, transaction_id)

    return jsonify({})


def _save_mbz_file(mbz_file, transaction_id):
    mbz_folder = os.path.join(app.config['UPLOAD_FOLDER'], transaction_id)
    if not os.path.isdir(mbz_folder):
        os.makedirs(mbz_folder)

    mbz_fullpath = os.path.join(mbz_folder, 'original_archive.mbz')
    mbz_file.save(mbz_fullpath)
    return mbz_fullpath


def _dl_and_save_ics_file(ics_url, transaction_id):
    ics_folder = os.path.join(app.config['UPLOAD_FOLDER'], transaction_id)

    if not os.path.isdir(ics_folder):
        os.makedirs(ics_folder)
    ics_fullpath = os.path.join(ics_folder, 'original_calendar.ics')

    r = requests.get(ics_url, stream=True)
    with open(ics_fullpath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
    return ics_fullpath


def _generate_transaction_uuid():
    return str(uuid.uuid4())


def _bad_request(msg=None):
    return jsonify({'message': 'Bad request.'}), 400


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)
    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
