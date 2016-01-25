#!/usr/bin/env python3
import uuid

from flask import Flask

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def hello():
    return 'hello'


def _generate_transaction_uuid():
    return str(uuid.uuid4())


def setup():
    return app

if __name__ == '__main__':
    setup().run(debug=True)
