import io
import os
import imp
import json
import shutil
import unittest
import course_activity_planner

from unittest.mock import MagicMock


class AppTest(unittest.TestCase):

    cal_url = 'https://calendar.google.com/calendar/ical/etsmtl.net_2ke' + \
        'm5ippvlh70v7pd6oo4ed9ig%40group.calendar.google.com/public/basic.ics'

    def setUp(self):
        self.app = course_activity_planner.setup('test')
        self.client = self.app.test_client()

    def tearDown(self):
        # TODO test on windows
        if os.path.isdir(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])
        imp.reload(course_activity_planner)  # Reset mocks on module

    def test_app_is_created(self):
        self.assertTrue(self.app)

    def test_generate_uuid(self):
        self.assertEqual(
            36, len(course_activity_planner._generate_transaction_uuid()))

    def test_cookie_is_set_after_posting_planning(self):
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value='')

        data = json.dumps({'ics_url': self.cal_url,
                          'planning': 'some planning'})
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
        data = json.dumps({'ics_url': self.cal_url,
                          'planning': 'some planning'})
        res = self.client.post('/api/planning', data=dict(data=data))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

        # No planning
        data = json.dumps({'ics_url': self.cal_url})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))
        self.assertEqual(400, res._status_code)
        assert 'Set-Cookie' not in res.headers

    def test_mbz_file_is_saved_after_posting_planning(self):
        course_activity_planner._generate_transaction_uuid = \
            MagicMock(return_value='uuid')

        data = json.dumps({'ics_url': self.cal_url,
                          'planning': 'some planning'})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        self.assertEqual(200, res._status_code)

        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_archive.mbz'))

        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_calendar.ics'))

if __name__ == '__main__':
    unittest.main()
