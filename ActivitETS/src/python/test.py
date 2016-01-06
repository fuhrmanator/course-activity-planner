#!/usr/bin/env python3
import unittest
from course_planner import MoodleCourse

moodle_archive_path = '../../test-data'


class TestDetectActivities(unittest.TestCase):

    def test_bad_archive_path(self):
        """Test constructor with an invalid path"""
        self.assertRaises(Exception, MoodleCourse, 'invalid_path')

    def test_get_quiz_count(self):
        course = MoodleCourse(moodle_archive_path)
        actual = course.get_quizes()
        self.assertEqual(3, len(actual))

    def test_get_quiz(self):
        course = MoodleCourse(moodle_archive_path)
        expected = ['quiz_146935', 'quiz_146936', 'quiz_146939']

        actual = course.get_quizes()
        self.assertEqual(expected, sorted(actual))

if __name__ == "__main__":
    unittest.main()
