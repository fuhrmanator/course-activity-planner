#!/usr/bin/env python3
import os
import unittest
import tarfile
import shutil
import tempfile
import arrow

from course_planner import MoodleCourse, CalendarReader, Seminar, Practica


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

    calendar_path = '../ActivitETS/multi-fr.ics'

    def setUp(self):
        self.calendar = CalendarReader(self.calendar_path)

    def test_event_count(self):
        meetings = self.calendar.get_all_meetings()
        self.assertEqual(13, len(meetings[Seminar]))
        self.assertEqual(13, len(meetings[Practica]))

        seminars = self.calendar.get_meetings_by_type(Seminar)
        practicas = self.calendar.get_meetings_by_type(Practica)
        self.assertEqual(13, len(seminars))
        self.assertEqual(13, len(practicas))

    def test_event_getters(self):
        seminars = self.calendar.get_meetings_by_type(Seminar)
        self.assertEqual(1389009600, seminars[0].calendar_event.begin.timestamp)

        expected = arrow.Arrow(2014, 4, 7, 12, 0, 0)
        self.assertEqual(expected, seminars[12].calendar_event.end)

        for i, s in enumerate(seminars):
            self.assertEqual('log210 Cours magistral %d' % (i + 1),
                             s.calendar_event.name)

if __name__ == "__main__":
    unittest.main()
