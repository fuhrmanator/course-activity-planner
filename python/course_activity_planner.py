#!/usr/bin/env python3
import uuid
import json
import os

from werkzeug import secure_filename
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

    transaction_id = _generate_transaction_uuid()
    session['transaction_id'] = transaction_id

    mbz_filename = secure_filename(mbz_file.filename)
    mbz_folder = os.path.join(app.config['UPLOAD_FOLDER'], transaction_id)

    os.makedirs(mbz_folder)
    mbz_fullpath = os.path.join(mbz_folder, 'original_archive.mbz')
    mbz_file.save(mbz_fullpath)

    return jsonify({})


def _generate_transaction_uuid():
    return str(uuid.uuid4())


def _bad_request(msg=None):
    return jsonify({'message': 'Bad request.'}), 400


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)
    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
