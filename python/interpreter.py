import re

from datetime import timedelta, datetime

from moodle import MoodleQuiz
from ics_calendar import Seminar, Practica


class AbsoluteTimeModifierException(Exception):
    """Raised if the absolute time has an invalid time format (24:00)"""
    def __init__(self, str):
        self.message = '\
Invalid absolute time modifier. Could not interpret value: "%s"' % str

    def __str__(self):
        return repr(self.message)


class InvalidSyntaxException(Exception):
    """Raised if the string could not be divided"""
    def __init__(self, str):
        self.message = '\
Invalid syntax while splitting events from string "%s"' % str

    def __str__(self):
        return repr(self.message)


class InvalidModifiersException(Exception):
    """Raised if modifiers could not be isolated or interpreted."""
    def __init__(self, str):
        self.message = '\
Invalid syntax while parsing modifiers from string "%s"' % str

    def __str__(self):
        return repr(self.message)


class Interpreter():

    modifiers_regex = re.compile(
        r'^[qsp][0-9]{1,2}(?P<end>[sf])?(?P<rel>[+-][0-9]+[wdhm])?' +
        r'(?:\@(?P<time>[0-9]{1,2}\:[0-9]{1,2}))?$', re.IGNORECASE)

    timedelta_regex = re.compile(
        r'^(?P<neg>\-)?\+?(:?(?P<weeks>[0-9])+w)?(:?(?P<days>[0-9])+d)?' +
        r'(:?(?P<hours>[0-9]+)h)?(:?(?P<minutes>[0-9]+)m)?$', re.IGNORECASE)

    candidates = {
        MoodleQuiz: re.compile(r'^[q](?P<id>[0-9]{1,2})([sf]?)', re.IGNORECASE),
        Seminar: re.compile(r'^[s](?P<id>[0-9]{1,2})([sf]?)', re.IGNORECASE),
        Practica: re.compile(r'^[p](?P<id>[0-9]{1,2})([sf]?)', re.IGNORECASE),
        }

    def __init__(self, meetings, course):
        self.meetings = meetings
        self.course = course

    def get_new_event_from_string(self, string):
        tokens = self._split_line(string)
        event = self._get_event_from_token(tokens[0])

        event.set_start_datetime(self._get_datetime_from_token(tokens[1]))
        event.set_end_datetime(self._get_datetime_from_token(tokens[2]))

        return event

    def _get_datetime_from_token(self, token):
        modifiers = self._get_modifiers_as_string(token)
        event = self._get_event_from_token(token)

        datetime = event.get_end_datetime() \
            if modifiers[0] else event.get_start_datetime()

        relative_mod = self._interpret_relative_modifier(modifiers[1])
        time_mod = self._interpret_time_modifier(modifiers[2])

        new_datetime = self._get_new_datetime(datetime, relative_mod, time_mod)

        return new_datetime

    def _get_event_from_token(self, token):
        event_clazz, event_id = self._detect_event_class_and_id(token)
        if event_clazz == MoodleQuiz:
            return self.course.get_activity_by_type_and_num(
                event_clazz, event_id)
        return self.meetings[event_clazz][event_id - 1]

    def _parse_subject(self, tokens):
        """Returns the event described by the first token of string
        """
        event_clazz, event_id = self._detect_event_class_and_id(tokens[0])
        return self.course.get_activity_by_type_and_num(event_clazz, event_id)

    def _detect_event_class_and_id(self, string):
        """Returns a tuple of the class and the meeting id."""
        for clazz, regex in self.candidates.items():
            r = regex.search(string)
            if r and r.groupdict()['id']:
                return (clazz, int(r.groupdict()['id']))

    def _split_line(self, string):
        parts = string.split(' ')

        if len(parts) != 3:
            raise InvalidSyntaxException(string)
        return parts

    def _get_modifiers_as_string(self, string):
        """Returns tuple (at_end, relative_modifier_str, time_modifier_str)

        at_end: True if the modifiers should be applied to the end of the
                event. False if the modifiers should be applied to the start
                of the event.

        relative_modifier_str: The delta to apply to the event start or end as a
                           string. Supports +/- w/d/h/m for weeks, days,
                           hours and minutes.
                           ex: '-2w', '-1d', '+15m', '+4h'

        time_modifier_str: None or a modifier of the final time as a string.
                       Must be applied last.
                       ex: @23:55
        """
        r = self.modifiers_regex.search(string)
        if not r:
            raise InvalidModifiersException(string)

        at_end = r.groupdict()['end'] == 'F'
        relative_modifier_str = r.groupdict()['rel']
        time_modifier_str = r.groupdict()['time']

        return (at_end, relative_modifier_str, time_modifier_str)

    def _interpret_time_modifier(self, time_modifier_str):
        if not time_modifier_str:
            return
        try:
            return datetime.strptime(time_modifier_str, '%H:%M').time()
        except Exception:
            raise AbsoluteTimeModifierException(time_modifier_str)

    def _interpret_relative_modifier(self, relative_modifier_str):
        if not relative_modifier_str:
            return

        r = self.timedelta_regex.search(relative_modifier_str)
        if not r:
            raise InvalidModifiersException(relative_modifier_str)

        negative_modifier = -1 if r.groupdict()['neg'] else 1

        weeks = int(r.groupdict()['weeks']) * negative_modifier \
            if r.groupdict()['weeks'] else 0

        days = int(r.groupdict()['days']) * negative_modifier \
            if r.groupdict()['days'] else 0

        hours = int(r.groupdict()['hours']) * negative_modifier \
            if r.groupdict()['hours'] else 0

        minutes = int(r.groupdict()['minutes']) * negative_modifier \
            if r.groupdict()['minutes'] else 0

        return timedelta(days=days, hours=hours, minutes=minutes, weeks=weeks)

    def _get_new_datetime(self, datetime, relative_mod, time_mod):
        """Build new datetime from relative and time modifiers."""
        if relative_mod:
            datetime += relative_mod

        if time_mod:
            return datetime.replace(hour=time_mod.hour, minute=time_mod.minute)

        return datetime
