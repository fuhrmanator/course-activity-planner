import unittest
import arrow

from dateutil import tz

from course_planner import Seminar, Practica, GenericMeeting
from calendar_reader import CalendarReader


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

        expected = arrow.get(
            2014, 4, 7, 8, 0, 0, tzinfo=tz.gettz('America/Montreal')).datetime

        meeting = GenericMeeting(seminars[12].calendar_event)
        actual = meeting.get_end_datetime()
        self.assertEqual(expected, actual)

        for i, s in enumerate(seminars):
            self.assertEqual('log210 Cours magistral %d' % (i + 1),
                             s.calendar_event.name)

if __name__ == "__main__":
    unittest.main()
