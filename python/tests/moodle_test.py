import unittest
import tarfile
import shutil
import tempfile

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


if __name__ == "__main__":
    unittest.main()
