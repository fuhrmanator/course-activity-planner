#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)


@app.route('/api/planning', methods=['POST'])
def hello():
    return 'hello'


def setup():
    return app

if __name__ == '__main__':
    setup().run(debug=True)
