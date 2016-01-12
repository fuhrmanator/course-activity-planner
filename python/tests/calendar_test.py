import unittest
import arrow

from course_planner import CalendarReader, Seminar, Practica


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
