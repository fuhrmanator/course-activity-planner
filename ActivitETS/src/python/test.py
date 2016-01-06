#!/usr/bin/env python3
import unittest
import course_planner

moodle_archive_path = '../../test-data'


class TestDetectActivities(unittest.TestCase):

    def test_get_quiz_count(self):
        actual = course_planner.get_quizes(moodle_archive_path)
        self.assertEqual(3, len(actual))

    def test_get_quiz(self):
        expected = ['quiz_146935', 'quiz_146936', 'quiz_146939']
        actual = course_planner.get_quizes(moodle_archive_path)
        self.assertEqual(expected, sorted(actual))

if __name__ == "__main__":
    unittest.main()
