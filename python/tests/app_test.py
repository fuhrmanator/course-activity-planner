import io
import os
import json
import shutil
import unittest
import course_activity_planner


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = course_activity_planner.setup('test')
        self.client = self.app.test_client()

    def tearDown(self):
        # TODO test on windows
        if os.path.isdir(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])

    def test_app_is_created(self):
        self.assertTrue(self.app)

    def test_generate_uuid(self):
        self.assertEqual(
            36, len(course_activity_planner._generate_transaction_uuid()))

    def test_cookie_is_set_after_posting_planning(self):
        data = json.dumps({'ics_url': '', 'planning': 'some planning'})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        self.assertEqual(200, res._status_code)
        assert res.headers['Set-Cookie'] is not None

    def test_cookie_is_not_set_after_bad_request(self):
        # No ICS, MBZ or planning
        res = self.client.post('/api/planning')
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No ICS url
        data = json.dumps({'planning': 'some planning'})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No MBZ
        data = json.dumps({'ics_url': '', 'planning': 'some planning'})
        res = self.client.post('/api/planning', data=dict(data=data))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No planning
        data = json.dumps({'ics_url': ''})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

if __name__ == '__main__':
    unittest.main()
