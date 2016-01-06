#!/usr/bin/env python3
import unittest
from course_planner import MoodleCourse

moodle_archive_path = 'test-data'


class TestDetectActivities(unittest.TestCase):

    def test_bad_archive_path(self):
        """Test constructor with an invalid path"""
        self.assertRaises(Exception, MoodleCourse, 'invalid_path')

    def test_get_quiz_count(self):
        course = MoodleCourse(moodle_archive_path)
        actual = course.get_quizzes()
        self.assertEqual(3, len(actual))

    def test_get_quizzes(self):
        course = MoodleCourse(moodle_archive_path)
        expected = ['quiz_146935', 'quiz_146936', 'quiz_146939']

        actual = course.get_quizzes()
        self.assertEqual(expected, sorted(actual))

    def test_get_quiz_by_module_id(self):
        course = MoodleCourse(moodle_archive_path)
        expected = '4271'

        actual = course.get_quiz_by_module_id('146935')['id']
        self.assertEqual(expected, actual)

    def test_get_quiz_by_module_id_get_data(self):
        course = MoodleCourse(moodle_archive_path)
        quiz = course.get_quiz_by_module_id('146935')

        self.assertEqual('test de remise', quiz['name'])
        self.assertEqual('1451709900', quiz['timeopen'])
        self.assertEqual('1454301900', quiz['timeclose'])


if __name__ == "__main__":
    unittest.main()
