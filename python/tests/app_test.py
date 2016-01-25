import io
import json
import unittest
import course_activity_planner

from werkzeug.datastructures import MultiDict


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = course_activity_planner.setup('test').test_client()

    def tearDown(self):
        pass

    def test_app_is_created(self):
        self.assertTrue(self.app)

    def test_generate_uuid(self):
        self.assertEqual(
            36, len(course_activity_planner._generate_transaction_uuid()))

    def test_cookie_is_set_after_posting_planning(self):
        res = self.app.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=json.dumps({'ics_url': ''})))

        self.assertEqual(200, res._status_code)
        assert res.headers['Set-Cookie'] is not None

    def test_cookie_is_not_set_after_bad_request(self):
        # no ICS or MBZ
        res = self.app.post('/api/planning')
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No ICS url
        res = self.app.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz')))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No MBZ
        res = self.app.post(
            '/api/planning',
            data=dict(data=json.dumps({'ics_url': ''})))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

if __name__ == '__main__':
    unittest.main()
