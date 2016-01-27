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
    db_path = '/tmp/test.db'

    def setUp(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
        self.app = course_activity_planner.setup('test')
        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.isdir(self.app.config['UPLOAD_FOLDER']):
            # TODO test on windows
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])
        course_activity_planner._clear_db()
        os.unlink(self.db_path)

        imp.reload(course_activity_planner)  # Reset mocks on module

    def test_app_is_created(self):
        self.assertTrue(self.app)

    def test_generate_uuid(self):
        self.assertEqual(
            36, len(course_activity_planner._generate_planning_uuid()))

    def test_new_planning(self):
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value='')

        data = json.dumps({'ics_url': self.cal_url})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        self.assertEqual(200, res._status_code)
        assert 'planning' in json.loads(res.data.decode('utf8'))

    def test_bad_requests_new_planning(self):
        # No ICS or MBZ
        res = self.client.post('/api/planning')
        self.assertEqual(400, res._status_code)

        # No ICS url
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=json.dumps({})))
        self.assertEqual(400, res._status_code)

        # No MBZ
        data = json.dumps({'ics_url': self.cal_url})
        res = self.client.post('/api/planning', data=dict(data=data))
        self.assertEqual(400, res._status_code)

    def test_files_are_saved_after_posting_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        data = json.dumps({'ics_url': self.cal_url})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        self.assertEqual(200, res._status_code)
        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_archive.mbz'))
        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_calendar.ics'))

    def test_planning_is_saved_to_db(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value='')

        data = json.dumps({'ics_url': self.cal_url,
                          'planning': 'some planning'})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        self.assertEqual(200, res._status_code)
        self.assertTrue(course_activity_planner._has_planning('uuid'))

    def test_planning_is_updated(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value='')

        data = json.dumps({'ics_url': self.cal_url})
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                      data=data))

        data = json.dumps({'planning': 'some text'})
        res = self.client.put(
            '/api/planning/uuid',
            data=data,
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(200, res._status_code)
        actual = course_activity_planner._get_planning('uuid').planning_txt
        self.assertEqual('some text', actual)

    def test_update_missing_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        data = json.dumps({'planning': 'some text'})
        res = self.client.put(
            '/api/planning/uuid',
            data=data,
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(404, res._status_code)

    def test_update_planning_bad_request(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        data = json.dumps({'planningee': 'some text'})
        res = self.client.put(
            '/api/planning/uuid',
            data=data,
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(400, res._status_code)

if __name__ == '__main__':
    unittest.main()
