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
    local_cal_path = '../data/multi-fr.ics'
    local_short_cal_path = '../data/short-fr.ics'
    local_mbz_path = '\
../data/backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz'

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
        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url))

        self.assertEqual(200, res._status_code)
        assert 'planning' in json.loads(res.data.decode('utf8'))

    def test_bad_requests_new_planning(self):
        # No ICS or MBZ
        res = self.client.post('/api/planning')
        self.assertEqual(400, res._status_code)

        # No ICS url
        res = self.client.post(
            '/api/planning',
            data=dict(file=(io.BytesIO(b'this is a test'), 'test.mbz')))
        self.assertEqual(400, res._status_code)

        # No MBZ
        res = self.client.post(
            '/api/planning', data=dict(ics_url=self.cal_url))
        self.assertEqual(400, res._status_code)

    def test_mbz_file_is_saved_after_posting_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url))

        self.assertEqual(200, res._status_code)
        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_archive.mbz'))

    def test_planning_is_saved_to_db(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url))

        self.assertEqual(200, res._status_code)
        self.assertTrue(course_activity_planner._has_planning('uuid'))

    def test_planning_is_updated(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1F S2'}),
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(200, res._status_code)
        actual = course_activity_planner._get_planning('uuid').planning_txt
        self.assertEqual('Q1 S1F S2', actual)

    def test_update_missing_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'some text'}),
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(404, res._status_code)

    def test_update_planning_bad_request(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planningee': 'some text'}),
            headers=[('Content-Type', 'application/json')])

        self.assertEqual(400, res._status_code)

    def test_inventory(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1 S2'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['inventory']

        expected = [
            {'key_str': 'P', 'rel_id': 1, 'title': 'log210 TP 1'},
            {'key_str': 'P', 'rel_id': 2, 'title': 'log210 TP 2'},
            {'key_str': 'P', 'rel_id': 3, 'title': 'log210 TP 3'},
            {'key_str': 'S', 'rel_id': 1, 'title': 'log210 Cours magistral 1'},
            {'key_str': 'S', 'rel_id': 2, 'title': 'log210 Cours magistral 2'},
            {'key_str': 'S', 'rel_id': 3, 'title': 'log210 Cours magistral 3'},
            {'key_str': 'H', 'rel_id': 1, 'title': 'Devoir bidon'},
            {'key_str': 'Q', 'rel_id': 1, 'title': 'test de remise'},
            {'key_str': 'Q', 'rel_id': 2, 'title': 'Premier test'},
            {'key_str': 'Q', 'rel_id': 3, 'title': 'Quiz Moodle Backup'},
        ]
        self.assertEqual(len(actual), len(expected))
        # no order expected
        assert all(x in expected for x in actual)

    def test_preview_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1 S2'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'key_str': 'Q', 'title': 'Quiz 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practica 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practica 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'Q', 'title': 'Quiz 1 closes',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practica 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practica 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practica 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practica 3 closes',
                'timestamp': 1390395600},
        ]
        self.assertEqual(expected, actual)

    def test_preview_homework_3_events(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'H1 S3F P3 P3F'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practica 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practica 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practica 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practica 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'H', 'title': 'Homework 1 opens',
                'timestamp': 1390222800},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practica 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'H', 'title': 'Homework 1 is due',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practica 3 closes',
                'timestamp': 1390395600},
            {'key_str': 'H', 'title': 'Homework 1 closes',
                'timestamp': 1390395600},
        ]
        self.assertEqual(len(actual), len(expected))
        # no order expected
        assert all(x in expected for x in actual)

    def test_preview_multiple_lines(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)
        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1 S2\nH1 S2 P3'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'title': 'Quiz 1 opens', 'timestamp': 1389009600,
                'key_str': 'Q'},
            {'title': 'Seminar 1 opens', 'timestamp': 1389009600,
                'key_str': 'S'},
            {'title': 'Seminar 1 closes', 'timestamp': 1389013200,
                'key_str': 'S'},
            {'title': 'Practica 1 opens', 'timestamp': 1389182400,
                'key_str': 'P'},
            {'title': 'Practica 1 closes', 'timestamp': 1389186000,
                'key_str': 'P'},
            {'title': 'Quiz 1 closes', 'timestamp': 1389614400,
                'key_str': 'Q'},
            {'title': 'Homework 1 opens', 'timestamp': 1389614400,
                'key_str': 'H'},
            {'title': 'Seminar 2 opens', 'timestamp': 1389614400,
                'key_str': 'S'},
            {'title': 'Seminar 2 closes', 'timestamp': 1389618000,
                'key_str': 'S'},
            {'title': 'Practica 2 opens', 'timestamp': 1389787200,
                'key_str': 'P'},
            {'title': 'Practica 2 closes', 'timestamp': 1389790800,
                'key_str': 'P'},
            {'title': 'Seminar 3 opens', 'timestamp': 1390219200,
                'key_str': 'S'},
            {'title': 'Seminar 3 closes', 'timestamp': 1390222800,
                'key_str': 'S'},
            {'title': 'Homework 1 is due', 'timestamp': 1390392000,
                'key_str': 'H'},
            {'title': 'Practica 3 opens', 'timestamp': 1390392000,
                'key_str': 'P'},
            {'title': 'Practica 3 closes', 'timestamp': 1390395600,
                'key_str': 'P'},
        ]
        self.assertEqual(expected, actual)

    def test_preview_planning_is_sorted(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        # Planning is not in chronological order
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q2 S1F S2\nQ1 S2F S3S'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'title': 'Seminar 1 opens', 'timestamp': 1389009600,
                'key_str': 'S'},
            {'title': 'Quiz 2 opens', 'timestamp': 1389013200,
                'key_str': 'Q'},
            {'title': 'Seminar 1 closes', 'timestamp': 1389013200,
                'key_str': 'S'},
            {'title': 'Practica 1 opens', 'timestamp': 1389182400,
                'key_str': 'P'},
            {'title': 'Practica 1 closes', 'timestamp': 1389186000,
                'key_str': 'P'},
            {'title': 'Quiz 2 closes', 'timestamp': 1389614400,
                'key_str': 'Q'},
            {'title': 'Seminar 2 opens', 'timestamp': 1389614400,
                'key_str': 'S'},
            {'title': 'Quiz 1 opens', 'timestamp': 1389618000,
                'key_str': 'Q'},
            {'title': 'Seminar 2 closes', 'timestamp': 1389618000,
                'key_str': 'S'},
            {'title': 'Practica 2 opens', 'timestamp': 1389787200,
                'key_str': 'P'},
            {'title': 'Practica 2 closes', 'timestamp': 1389790800,
                'key_str': 'P'},
            {'title': 'Quiz 1 closes', 'timestamp': 1390219200,
                'key_str': 'Q'},
            {'title': 'Seminar 3 opens', 'timestamp': 1390219200,
                'key_str': 'S'},
            {'title': 'Seminar 3 closes', 'timestamp': 1390222800,
                'key_str': 'S'},
            {'title': 'Practica 3 opens', 'timestamp': 1390392000,
                'key_str': 'P'},
            {'title': 'Practica 3 closes', 'timestamp': 1390395600,
                'key_str': 'P'},
        ]
        self.assertEqual(expected, actual)

    def test_warnings_are_sent_if_end_is_before_start(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S2 S1'}),
            headers=[('Content-Type', 'application/json')])

        res = self.client.get('/api/planning/uuid/preview')
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['alerts']

        expected = [{'type': 'warning',
                    'msg': 'Quiz 1 ends before it starts.'}]
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
