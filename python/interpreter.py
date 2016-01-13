import re

from course_planner import MoodleQuiz, Seminar, Practica


class Interpreter():

    candidates = {
        MoodleQuiz: re.compile(r'^[q]([0-9]{1,2})([sf]?)$', re.IGNORECASE),
        Seminar: re.compile(r'^[s]([0-9]{1,2})([sf]?)$', re.IGNORECASE),
        Practica: re.compile(r'^[p]([0-9]{1,2})([sf]?)$', re.IGNORECASE),
        }

    def __init__(self, meetings, course):
        self.meetings = meetings
        self.course = course

    def _detect_event_class_and_id(self, string):
        """Returns a tuple of the class and the meeting id."""
        for clazz, regex in self.candidates.items():
            r = regex.search(string)
            if r:
                return (clazz, int(r.groups()[0]))

    def _split_line(self, string):
        parts = string.split(' ')

        if len(parts) != 3:
            raise Exception('Invalid syntax while splitting events.')
        return parts

    def _get_modifiers(self, string):
        """Returns tuple (at_end, relative_modifier, time_modifier)

        at_end: True if the modifiers should be applied to the end of the
                event. False if the modifiers should be applied to the start
                of the event.

        relative_modifier: The delta to apply to the event start or end.
                           Supports +/- d/h/m for days, hours, minutes.
                           ex: '-1d', '+15m', '+4h'

        time_modifier: None or a modifier of the final time. Must be applied
                       last.
                       ex: @23:55
        """
        regex = re.compile(
            r'^[qsp][0-9]{1,2}(?P<end>[sf])?(?P<rel>[+-][0-9]+[dmh])?' +
            r'(?:\@(?P<time>[0-9]{1,2}\:[0-9]{1,2}))?$', re.IGNORECASE)

        r = regex.search(string)
        if not r:
            raise Exception('Invalid syntax while parsing modifiers.')

        at_end = r.groupdict()['end'] == 'F'

        relative_modifier = r.groupdict()['rel']

        return (at_end, relative_modifier, None)
