import re
import arrow

from ics import Calendar as iCalendar
from common import Event, CAPException


class InvalidCalendarFileException(CAPException):
    """Raised if the calendar file could not read"""


class GenericMeeting(Event):
    def __init__(self, calendar_event):
        self.calendar_event = calendar_event

    def get_start_datetime(self):
        return self.calendar_event.begin.to('America/Montreal').datetime

    def get_start_timestamp(self):
        return self.calendar_event.begin.to('America/Montreal').timestamp

    def get_end_datetime(self):
        return self.calendar_event.end.to('America/Montreal').datetime

    def get_end_timestamp(self):
        return self.calendar_event.end.to('America/Montreal').timestamp

    def set_start_datetime(self, datetime):
        self.calendar_event.begin = arrow.get(datetime)

    def get_title(self):
        return self.calendar_event.name


class Seminar(GenericMeeting):
    def __init__(self, *args, **kwargs):
        GenericMeeting.__init__(self, *args, **kwargs)

    def get_key(self):
        return 'S'


class Practica(GenericMeeting):
    def __init__(self, *args, **kwargs):
        GenericMeeting.__init__(self, *args, **kwargs)

    def get_key(self):
        return 'P'


class CalendarReader():
    """Reads iCalendar and returns generic meetings"""

    # Association of the meeting classes and their regex in the calendar
    candidates = {Seminar: re.compile(r'Cours magistral ([0-9]{1,2})$'),
                  Practica: re.compile(r'TP ([0-9]{1,2})$')}

    def __init__(self, calendar_path):
        with open(calendar_path, 'r') as cal_file:
            try:
                cal_content = cal_file.readlines()
                self.calendar = iCalendar(cal_content)
            except Exception:
                raise InvalidCalendarFileException()

    def get_all_meetings(self):
        """Parses events from ics_calendar and orders them by meeting type.
        All meetings are returned in a dict of arrays with the meeting class
        as the key.
        """
        generic_meetings = {}

        for candidate_class in self.candidates.keys():
            generic_meetings[candidate_class] = []

        for meeting in self.calendar.events:
            for candidate_class, regex in self.candidates.items():
                r = regex.search(meeting.name)
                if r:
                    meeting_instance = candidate_class(meeting)
                    generic_meetings[candidate_class].append(meeting_instance)

        return generic_meetings

    def get_meetings_by_type(self, candidate):
        """Return a list of the filtered meetings fitting the candidate's regex
        """
        generic_meetings = []

        for meeting in self.calendar.events:
            if self.candidates[candidate].search(meeting.name):
                r = self.candidates[candidate].search(meeting.name)
                if r:
                    meeting_instance = candidate(meeting)
                    generic_meetings.append(meeting_instance)

        return generic_meetings
