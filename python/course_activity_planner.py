#!/usr/bin/env python3
import uuid

from flask import Flask, session, jsonify, request

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def post_planning():
    req = request.get_json()
    if not req or 'ics_url' not in req:
        return jsonify({'message': 'Bad request'}), 400

    session['transaction_id'] = _generate_transaction_uuid()
    return jsonify({})


def _generate_transaction_uuid():
    return str(uuid.uuid4())


def setup(env):
    app.config.from_pyfile('config/%s.py' % env)
    return app

if __name__ == '__main__':
    setup('dev').run(debug=True)
