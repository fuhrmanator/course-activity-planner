import unittest
import tarfile
import shutil
import tempfile
import os

import xml.etree.ElementTree as ET

from course_planner import MoodleCourse, MoodleQuiz


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

    def test_load_section_order(self):
        course = MoodleCourse(self.tmp_path)
        actual = course._load_section_order()

        self.assertEqual([146934, 146935, 146936, 146937, 146939], actual)

    def test_load_activities(self):
        course = MoodleCourse(self.tmp_path)
        actual = course._load_activites()[MoodleQuiz]
        self.assertEqual(3, len(actual))

    def test_sort_activity_type(self):
        course = MoodleCourse(self.tmp_path)
        activities = course._load_activites()[MoodleQuiz]
        activities = course._sort_activity_type(activities)

        for i, x in enumerate([146935, 146936, 146939]):
            self.assertEqual(x, activities[i]['moduleid'])

    # def test_get_quizzes(self):
    #     course = MoodleCourse(self.tmp_path)
    #     expected = ['146935', '146936', '146939']
    #
    #     actual = course._get_quizzes_module_id()
    #     self.assertEqual(expected, sorted(actual))

    # def test_get_quiz_by_relative_num(self):
    #     course = MoodleCourse(self.tmp_path)
    #     expected = '4271'
    #
    #     actual = course.get_activity_by_type_and_num(MoodleQuiz, 1)['id']
    #     self.assertEqual(expected, actual)

    # def test_get_quiz_by_module_id_get_data(self):
    #     course = MoodleCourse(self.tmp_path)
    #     quiz = course.get_quiz_by_module_id('146935')
    #
    #     self.assertEqual('test de remise', quiz['name'])
    #     self.assertEqual('1451709900', quiz['timeopen'])
    #     self.assertEqual('1454301900', quiz['timeclose'])
    #
    # def test_set_quiz_dates(self):
    #     course = MoodleCourse(self.tmp_path)
    #     quiz = course.get_quiz_by_module_id('146935')
    #
    #     self.assertEqual('1451709900', quiz['timeopen'])
    #     self.assertEqual('1454301900', quiz['timeclose'])
    #
    #     quiz['timeopen'] = '42424242'
    #     quiz['timeclose'] = '4242424242'
    #
    #     self.assertEqual('42424242', quiz['timeopen'])
    #     self.assertEqual('4242424242', quiz['timeclose'])
    #
    # def test_set_invalid_key_raises_exception(self):
    #     course = MoodleCourse(self.tmp_path)
    #     quiz = course.get_quiz_by_module_id('146935')
    #
    #     with self.assertRaises(Exception):
    #         quiz['invalid_key'] = 'some data'


if __name__ == "__main__":
    unittest.main()
