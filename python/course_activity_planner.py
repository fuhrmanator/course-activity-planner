#!/usr/bin/env python3
import uuid
import json

from flask import Flask, session, jsonify, request

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def post_planning():
    req = json.loads(request.form['data'])
    if not req or 'ics_url' not in req:
        return _bad_request()

    f = request.files['file']
    if not f:
        return _bad_request()

    session['transaction_id'] = _generate_transaction_uuid()
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
