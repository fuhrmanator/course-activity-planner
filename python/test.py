#!/usr/bin/env python3
import os
import unittest
import tarfile
import shutil
import tempfile
import arrow

from ics import Calendar

from course_planner import MoodleCourse


class TestQuiz(unittest.TestCase):

    moodle_archive_path = '\
../backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz'

    def setUp(self):
        self.tmp_path = tempfile.mkdtemp()

        with tarfile.open(self.moodle_archive_path) as tar_file:
            tar_file.extractall(self.tmp_path)

    def tearDown(self):
        # TODO test on windows
        shutil.rmtree(self.tmp_path)

    def test_bad_archive_path(self):
        """Test constructor with an invalid path"""
        self.assertRaises(Exception, MoodleCourse, 'invalid_path')

    def test_get_quiz_count(self):
        course = MoodleCourse(self.tmp_path)
        actual = course.get_quizzes()
        self.assertEqual(3, len(actual))

    def test_get_quizzes(self):
        course = MoodleCourse(self.tmp_path)
        expected = ['quiz_146935', 'quiz_146936', 'quiz_146939']

        actual = course.get_quizzes()
        self.assertEqual(expected, sorted(actual))

    def test_get_quiz_by_module_id(self):
        course = MoodleCourse(self.tmp_path)
        expected = '4271'

        actual = course.get_quiz_by_module_id('146935')['id']
        self.assertEqual(expected, actual)

    def test_get_quiz_by_module_id_get_data(self):
        course = MoodleCourse(self.tmp_path)
        quiz = course.get_quiz_by_module_id('146935')

        self.assertEqual('test de remise', quiz['name'])
        self.assertEqual('1451709900', quiz['timeopen'])
        self.assertEqual('1454301900', quiz['timeclose'])

    def test_set_quiz_dates(self):
        course = MoodleCourse(self.tmp_path)
        quiz = course.get_quiz_by_module_id('146935')

        self.assertEqual('1451709900', quiz['timeopen'])
        self.assertEqual('1454301900', quiz['timeclose'])

        quiz['timeopen'] = '42424242'
        quiz['timeclose'] = '4242424242'

        self.assertEqual('42424242', quiz['timeopen'])
        self.assertEqual('4242424242', quiz['timeclose'])

    def test_set_invalid_key_raises_exception(self):
        course = MoodleCourse(self.tmp_path)
        quiz = course.get_quiz_by_module_id('146935')

        with self.assertRaises(Exception):
            quiz['invalid_key'] = 'some data'


class TestCalendarParsing(unittest.TestCase):

    calendar_path = '../ActivitETS/basic.ics'

    def setUp(self):
        self.tmp_file = tempfile.mktemp()

        with open(self.calendar_path, 'r') as cal_file:
            cal_content = cal_file.readlines()
            self.calendar = Calendar(cal_content)

    def tearDown(self):
        if os.path.isfile(self.tmp_file):
            os.remove(self.tmp_file)

    def test_event_count(self):
        self.assertEqual(13, len(self.calendar.events))

    def test_event_getters(self):
        self.assertEqual(1430328600, self.calendar.events[0].begin.timestamp)

        expected = arrow.Arrow(2015, 7, 29, 21, 0, 0)
        self.assertEqual(expected, self.calendar.events[12].end)

        index = 0
        for event in self.calendar.events:
            self.assertEqual('LOG210-01 Séance {0:02d}'.format(index + 1),
                             self.calendar.events[index].name)

if __name__ == "__main__":
    unittest.main()
