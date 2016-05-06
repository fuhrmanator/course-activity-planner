import io
import os
import imp
import json
import shutil
import unittest
import base64
import tarfile
import course_activity_planner

from unittest.mock import MagicMock

from moodle import MoodleCourse, MoodleQuiz


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
        self.token = course_activity_planner._create_token(111)

        # Ignore ics url in request and link to local ics file
        course_activity_planner._dl_and_save_ics_file = \
            MagicMock(return_value=self.local_short_cal_path)

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
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url,
                name='LOG-121',
                year='2016',
                semester='02',
                group='06'
                ),
            headers=[('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(200, res._status_code)
        planning = json.loads(res.data.decode('utf8'))['planning']
        self.assertEqual('LOG-121', planning['name'])
        self.assertEqual('2016', planning['year'])
        self.assertEqual('02', planning['semester'])
        self.assertEqual('06', planning['group'])

    def test_new_planning_without_mbz(self):
        res = self.client.post(
            '/api/planning',
            data=dict(ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(200, res._status_code)
        assert 'planning' in json.loads(res.data.decode('utf8'))

    def test_get_planning_bad_request(self):
        # Test getting a planning that doesn't exist
        res = self.client.get(
            '/api/planning/uuid2',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(404, res._status_code)

    def test_get_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

    def test_get_plannings_for_user(self):
        # Test 0 plannings are returned
        res = self.client.get(
            '/api/planning/',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['plannings']
        self.assertEqual(0, len(actual))

        # Create first planning
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        # Test 1 planning is returned
        res = self.client.get(
            '/api/planning/',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['plannings']
        self.assertEqual(1, len(actual))

        # Create second planning
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid2')
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        # Test 2 plannings are returned
        res = self.client.get(
            '/api/planning/',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['plannings']
        self.assertEqual(2, len(actual))

    def test_bad_requests_new_planning(self):
        # No ICS or MBZ
        res = self.client.post(
            '/api/planning',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(400, res._status_code)

        # No ICS url
        res = self.client.post(
            '/api/planning',
            data=dict(mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz')),
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(400, res._status_code)

    def test_mbz_file_is_saved_after_posting_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(200, res._status_code)
        self.assertTrue(os.path.exists('\
/tmp/course_activity_planner_test/uuid/original_archive.mbz'))

    def test_planning_is_saved_to_db(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(200, res._status_code)
        self.assertTrue(course_activity_planner._has_planning('uuid'))

    def test_planning_is_updated_in_memory(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1F S2'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(202, res._status_code)
        actual = course_activity_planner. \
            _get_planning_bypass('uuid').planning_txt
        self.assertEqual('Q1 S1F S2', actual)

    def test_invalid_date_count_update(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1F S2S-30m s3'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        # At this point, the planning might be errored
        # but it will only be detected at the next preview
        self.assertEqual(202, res._status_code)

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['alerts']
        self.assertEqual(1, len(actual))
        msg = actual[0]['msg']
        self.assertEqual('Activity "MoodleQuiz" must have between ' +
                         '2 and 2 dates. 3 given.', msg)

    def test_trailing_spaces_should_not_affect_cap(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1F S2S-30m  \nMq2 s2 s3'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(202, res._status_code)

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['alerts']
        self.assertEqual(0, len(actual))

    def test_multiple_spaces_should_not_affect_cap(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1  S1F    S2S-30m'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(202, res._status_code)

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['alerts']
        self.assertEqual(0, len(actual))

    def test_update_missing_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'some text'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(404, res._status_code)

    def test_delete_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)
        # Planning exists
        res = self.client.get(
            '/api/planning/uuid',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        # Delete planning
        res = self.client.delete(
            '/api/planning/uuid',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(204, res._status_code)

        # Planning was deleted
        res = self.client.get(
            '/api/planning/uuid',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(404, res._status_code)

    def test_unauthorized_access(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        # Simulate another client with other user id
        unauthorized_token = course_activity_planner._create_token(1111)
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'some text'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % unauthorized_token)])
        self.assertEqual(403, res._status_code)

    def test_update_planning_bad_request(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planningee': 'some text'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(400, res._status_code)

    def test_inventory(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'Q1 S1 S2'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual_cal = json.loads(
            res.data.decode('utf8'))['inventory']['meetings']
        actual_moodle = json.loads(
            res.data.decode('utf8'))['inventory']['activities']

        expected_cal = [
            {'key_str': 'S', 'rel_id': 1, 'title': 'log210 Cours magistral 1'},
            {'key_str': 'S', 'rel_id': 2, 'title': 'log210 Cours magistral 2'},
            {'key_str': 'S', 'rel_id': 3, 'title': 'log210 Cours magistral 3'},
            {'key_str': 'P', 'rel_id': 1, 'title': 'log210 TP 1'},
            {'key_str': 'P', 'rel_id': 2, 'title': 'log210 TP 2'},
            {'key_str': 'P', 'rel_id': 3, 'title': 'log210 TP 3'},
        ]
        expected_moodle = [
            {'key_str': 'MH', 'rel_id': 1, 'title': 'Devoir bidon'},
            {'key_str': 'MQ', 'rel_id': 1, 'title': 'test de remise'},
            {'key_str': 'MQ', 'rel_id': 2, 'title': 'Premier test'},
            {'key_str': 'MQ', 'rel_id': 3, 'title': 'Quiz Moodle Backup'},
        ]
        self.assertEqual(len(actual_cal), len(expected_cal))
        self.assertEqual(len(actual_moodle), len(expected_moodle))
        # no order expected
        assert all(x in expected_cal for x in actual_cal)
        assert all(x in expected_moodle for x in actual_moodle)

    def test_get_bad_preview(self):
        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(404, res._status_code)

    def test_preview_planning(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1 S2'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'key_str': 'MQ', 'title': 'Quiz 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practicum 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practicum 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'MQ', 'title': 'Quiz 1 closes',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practicum 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practicum 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practicum 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practicum 3 closes',
                'timestamp': 1390395600},
        ]
        self.assertEqual(expected, actual)

    def test_preview_planning_without_mbz(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']
        expected = [
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practicum 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practicum 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practicum 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practicum 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practicum 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practicum 3 closes',
                'timestamp': 1390395600},
        ]
        self.assertEqual(expected, actual)

    def test_update_planning_without_mbz(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']
        self.assertEqual(12, len(actual))

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S2'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']
        self.assertEqual(14, len(actual))

    def test_preview_planning_with_invalid_mbz(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])

        self.assertEqual(400, res._status_code)
        actual = json.loads(res.data.decode('utf8'))['alerts']
        self.assertEqual(1, len(actual))
        msg = actual[0]['msg']
        self.assertEqual('MBZ file could not be read.', msg)

    def test_preview_homework_3_events(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MH1 S3F P3 P3F'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practicum 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practicum 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practicum 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practicum 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'MH', 'title': 'Homework 1 opens',
                'timestamp': 1390222800},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practicum 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'MH', 'title': 'Homework 1 is due',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practicum 3 closes',
                'timestamp': 1390395600},
            {'key_str': 'MH', 'title': 'Homework 1 closes',
                'timestamp': 1390395600},
        ]

        self.assertEqual(len(actual), len(expected))
        # no order expected
        assert all(x in expected for x in actual)

    def test_preview_multiple_lines(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1 S2\nMH1 S2 P3'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'title': 'Quiz 1 opens', 'timestamp': 1389009600,
                'key_str': 'MQ'},
            {'title': 'Seminar 1 opens', 'timestamp': 1389009600,
                'key_str': 'S'},
            {'title': 'Seminar 1 closes', 'timestamp': 1389013200,
                'key_str': 'S'},
            {'title': 'Practicum 1 opens', 'timestamp': 1389182400,
                'key_str': 'P'},
            {'title': 'Practicum 1 closes', 'timestamp': 1389186000,
                'key_str': 'P'},
            {'title': 'Quiz 1 closes', 'timestamp': 1389614400,
                'key_str': 'MQ'},
            {'title': 'Homework 1 opens', 'timestamp': 1389614400,
                'key_str': 'MH'},
            {'title': 'Seminar 2 opens', 'timestamp': 1389614400,
                'key_str': 'S'},
            {'title': 'Seminar 2 closes', 'timestamp': 1389618000,
                'key_str': 'S'},
            {'title': 'Practicum 2 opens', 'timestamp': 1389787200,
                'key_str': 'P'},
            {'title': 'Practicum 2 closes', 'timestamp': 1389790800,
                'key_str': 'P'},
            {'title': 'Seminar 3 opens', 'timestamp': 1390219200,
                'key_str': 'S'},
            {'title': 'Seminar 3 closes', 'timestamp': 1390222800,
                'key_str': 'S'},
            {'title': 'Homework 1 is due', 'timestamp': 1390392000,
                'key_str': 'MH'},
            {'title': 'Practicum 3 opens', 'timestamp': 1390392000,
                'key_str': 'P'},
            {'title': 'Practicum 3 closes', 'timestamp': 1390395600,
                'key_str': 'P'},
        ]
        self.assertEqual(expected, actual)

    def test_preview_planning_is_sorted(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        # Planning is not in chronological order
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ2 S1F S2\nMQ1 S2F S3S'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'title': 'Seminar 1 opens', 'timestamp': 1389009600,
                'key_str': 'S'},
            {'title': 'Quiz 2 opens', 'timestamp': 1389013200,
                'key_str': 'MQ'},
            {'title': 'Seminar 1 closes', 'timestamp': 1389013200,
                'key_str': 'S'},
            {'title': 'Practicum 1 opens', 'timestamp': 1389182400,
                'key_str': 'P'},
            {'title': 'Practicum 1 closes', 'timestamp': 1389186000,
                'key_str': 'P'},
            {'title': 'Quiz 2 closes', 'timestamp': 1389614400,
                'key_str': 'MQ'},
            {'title': 'Seminar 2 opens', 'timestamp': 1389614400,
                'key_str': 'S'},
            {'title': 'Quiz 1 opens', 'timestamp': 1389618000,
                'key_str': 'MQ'},
            {'title': 'Seminar 2 closes', 'timestamp': 1389618000,
                'key_str': 'S'},
            {'title': 'Practicum 2 opens', 'timestamp': 1389787200,
                'key_str': 'P'},
            {'title': 'Practicum 2 closes', 'timestamp': 1389790800,
                'key_str': 'P'},
            {'title': 'Quiz 1 closes', 'timestamp': 1390219200,
                'key_str': 'MQ'},
            {'title': 'Seminar 3 opens', 'timestamp': 1390219200,
                'key_str': 'S'},
            {'title': 'Seminar 3 closes', 'timestamp': 1390222800,
                'key_str': 'S'},
            {'title': 'Practicum 3 opens', 'timestamp': 1390392000,
                'key_str': 'P'},
            {'title': 'Practicum 3 closes', 'timestamp': 1390395600,
                'key_str': 'P'},
        ]
        self.assertEqual(expected, actual)

    def test_warnings_are_sent_if_end_is_before_start(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S2 S1'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['alerts']

        expected = [{'type': 'warning',
                    'msg': 'Quiz 1 ends before it starts.'}]
        self.assertEqual(expected, actual)

    def test_new_mbz_archive(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url=self.cal_url),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1F S2\nE1 S1F S2'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/mbz',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        new_mbz_path = os.path.join(self.app.config['UPLOAD_FOLDER'],
                                    'downloaded.mbz')

        encoded = json.loads(res.data.decode('utf8'))['mbz_64']
        with open(new_mbz_path, 'wb') as f:
            f.write(base64.b64decode(encoded))

        print(os.path.exists(new_mbz_path))
        tmp_archive = os.path.join(self.app.config['UPLOAD_FOLDER'],
                                   'extracted')

        with tarfile.open(new_mbz_path) as tar_file:
            tar_file.extractall(tmp_archive)
            course = MoodleCourse(tmp_archive)
            quiz = course.get_activity_by_type_and_num(MoodleQuiz, 1)

            expected_s = 1389013200
            expected_e = 1389614400

            actual_s = quiz.get_start_timestamp()
            actual_e = quiz.get_end_timestamp()

            self.assertEqual(expected_s, actual_s)
            self.assertEqual(expected_e, actual_e)

    def test_preview_planning_with_exam(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S1F'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/preview',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['preview']

        expected = [
            {'key_str': 'E', 'title': 'Exam 1 starts',
                'timestamp': 1389009600},
            {'key_str': 'S', 'title': 'Seminar 1 opens',
                'timestamp': 1389009600},
            {'key_str': 'E', 'title': 'Exam 1 ends',
                'timestamp': 1389013200},
            {'key_str': 'S', 'title': 'Seminar 1 closes',
                'timestamp': 1389013200},
            {'key_str': 'P', 'title': 'Practicum 1 opens',
                'timestamp': 1389182400},
            {'key_str': 'P', 'title': 'Practicum 1 closes',
                'timestamp': 1389186000},
            {'key_str': 'S', 'title': 'Seminar 2 opens',
                'timestamp': 1389614400},
            {'key_str': 'S', 'title': 'Seminar 2 closes',
                'timestamp': 1389618000},
            {'key_str': 'P', 'title': 'Practicum 2 opens',
                'timestamp': 1389787200},
            {'key_str': 'P', 'title': 'Practicum 2 closes',
                'timestamp': 1389790800},
            {'key_str': 'S', 'title': 'Seminar 3 opens',
                'timestamp': 1390219200},
            {'key_str': 'S', 'title': 'Seminar 3 closes',
                'timestamp': 1390222800},
            {'key_str': 'P', 'title': 'Practicum 3 opens',
                'timestamp': 1390392000},
            {'key_str': 'P', 'title': 'Practicum 3 closes',
                'timestamp': 1390395600},
        ]
        self.assertEqual(expected, actual)

    def test_download_planets_without_group(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S1F "Examen Intra 1"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = 'Examen Intra 1, lundi le 06 janvier' \
            ' 2014 de 7h à 8h'
        self.assertEqual(expected, actual)

    def test_download_planets(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        # Ignore mbz in request and link to local mbz file
        course_activity_planner._save_mbz_file = \
            MagicMock(return_value=self.local_mbz_path)

        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='some_url_to_be_mocked', group='1'),
            headers=[('Authorization', "Bearer %s" % self.token)])

        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S1F "Examen Intra 1"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = 'Examen Intra 1, Groupe 1, lundi le 06 janvier' \
            ' 2014 de 7h à 8h'
        self.assertEqual(expected, actual)

        # Test minutes
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1+1m S1F-1m "Examen Intra 1"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = 'Examen Intra 1, Groupe 1, lundi le 06 janvier' \
            ' 2014 de 7h01 à 7h59'
        self.assertEqual(expected, actual)

        # Test different days
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S1+1d@15:01 "Examen Intra 1"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = 'Examen Intra 1, Groupe 1, du lundi 06 janvier 2014 7h ' \
            'au mardi 07 janvier 2014 15h01'

        # Test multiple lines
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'E1 S1 S1F "Examen Intra 1"\n' +
                             'E2 S2 S2F "Examen Intra 2"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = \
            'Examen Intra 1, Groupe 1, lundi le 06 janvier 2014 de 7h à 8h' \
            '\nExamen Intra 2, Groupe 1, lundi le 13 janvier 2014 de 7h à 8h'
        self.assertEqual(expected, actual)

        # Test moodle activity
        res = self.client.put(
            '/api/planning/uuid',
            data=json.dumps({'planning': 'MQ1 S1 S1F "Quiz important 1"'}),
            headers=[('Content-Type', 'application/json'),
                     ('Authorization', "Bearer %s" % self.token)])

        res = self.client.get(
            '/api/planning/uuid/planets',
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['planets']
        expected = \
            'Quiz important 1, Groupe 1, lundi le 06 janvier 2014 de 7h à 8h'
        self.assertEqual(expected, actual)


class AppTestNoURLMock(unittest.TestCase):
    db_path = '/tmp/test.db'

    def setUp(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
        self.app = course_activity_planner.setup('test')
        self.client = self.app.test_client()
        self.token = course_activity_planner._create_token(111)

    def tearDown(self):
        if os.path.isdir(self.app.config['UPLOAD_FOLDER']):
            # TODO test on windows
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])
        course_activity_planner._clear_db()
        os.unlink(self.db_path)

        imp.reload(course_activity_planner)  # Reset mocks on module

    def test_planning_with_invalid_ics_url(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_url='http://some_invalid_url'),
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(400, res._status_code)

        actual = json.loads(res.data.decode('utf8'))['alerts']
        self.assertEqual(1, len(actual))
        msg = actual[0]['msg']
        self.assertEqual('Calendar file is not a valid ICS file.', msg)

        res = self.client.get('/api/planning/uuid',
                              headers=[('Authorization',
                                        "Bearer %s" % self.token)])
        self.assertEqual(404, res._status_code)

    def test_planning_with_ics_file(self):
        course_activity_planner._generate_planning_uuid = \
            MagicMock(return_value='uuid')
        res = self.client.post(
            '/api/planning',
            data=dict(
                mbz_file=(io.BytesIO(b'this is a test'), 'test.mbz'),
                ics_file=(io.BytesIO(b'this is a test'), 'test.ics')),
            headers=[('Authorization', "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

        res = self.client.get('/api/planning/uuid',
                              headers=[('Authorization',
                                        "Bearer %s" % self.token)])
        self.assertEqual(200, res._status_code)

if __name__ == '__main__':
    unittest.main()
