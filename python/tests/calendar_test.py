import unittest
import arrow

from dateutil import tz

from ics_calendar import CalendarReader, Seminar, Practicum, Laboratory, \
    GenericMeeting


class TestCalendarParsing(unittest.TestCase):

    calendar_path = '../data/multi-fr.ics'

    def setUp(self):
        self.calendar = CalendarReader(self.calendar_path)

    def test_event_count(self):
        meetings = self.calendar.get_all_meetings()
        self.assertEqual(13, len(meetings[Seminar]))
        self.assertEqual(13, len(meetings[Practicum]))
        self.assertEqual(13, len(meetings[Laboratory]))

        seminars = self.calendar.get_meetings_by_type(Seminar)
        practica = self.calendar.get_meetings_by_type(Practicum)
        laboratories = self.calendar.get_meetings_by_type(Laboratory)
        self.assertEqual(13, len(seminars))
        self.assertEqual(13, len(practica))
        self.assertEqual(13, len(laboratories))

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
