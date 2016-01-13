import unittest
import tarfile
import shutil
import tempfile

from interpreter import Interpreter
from course_planner import CalendarReader, MoodleCourse, MoodleQuiz, Seminar, \
    Practica


class InterpreterTest(unittest.TestCase):

    calendar_path = '../ActivitETS/multi-fr.ics'
    moodle_archive_path = '\
../backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz'

    def setUp(self):
        # Setup calendar
        calendar = CalendarReader(self.calendar_path)

        self.calendar_meetings = calendar.get_all_meetings()

        # Setup Moodle course
        self.tmp_path = tempfile.mkdtemp()
        with tarfile.open(self.moodle_archive_path) as tar_file:
            tar_file.extractall(self.tmp_path)

        self.course = MoodleCourse(self.tmp_path)
        self.interpreter = Interpreter(self.calendar_meetings, self.course)

    def tearDown(self):
        # TODO test on windows
        shutil.rmtree(self.tmp_path)

    def test_invalid_syntax(self):
        self.assertRaises(
            Exception, self.interpreter._split_line, 'Q1S1FS2S')

    def test_split_events_line(self):
        self.assertEqual(['Q1', 'S1F', 'S2S'],
                         self.interpreter._split_line('Q1 S1F S2S'))

    def test_detection_of_event(self):
        event = self.interpreter._detect_event_class_and_id('Q1')
        self.assertEqual((MoodleQuiz, 1), event)

        event = self.interpreter._detect_event_class_and_id('q13')
        self.assertEqual((MoodleQuiz, 13), event)

        event = self.interpreter._detect_event_class_and_id('p2')
        self.assertEqual((Practica, 2), event)

        event = self.interpreter._detect_event_class_and_id('P12')
        self.assertEqual((Practica, 12), event)

        event = self.interpreter._detect_event_class_and_id('s4')
        self.assertEqual((Seminar, 4), event)

        event = self.interpreter._detect_event_class_and_id('S4')
        self.assertEqual((Seminar, 4), event)

    def test_get_modifiers(self):
        mods = self.interpreter._get_modifiers('S1F+1D@23:59')

        at_end = mods[0]
        self.assertEqual(True, at_end)

        mods = self.interpreter._get_modifiers('S1S+1D@23:59')

        at_end = mods[0]
        self.assertEqual(False, at_end)
