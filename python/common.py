import arrow
import json

from flask import Response


class InvalidSyntaxException(Exception):
    """Raised if the string could not be divided"""
    def __init__(self, str):
        self.message = '\
Invalid syntax while splitting events from string "%s"' % str

    def __str__(self):
        return repr(self.message)


class Event():
    """Abstract class to be extended with all event (activity or meeting)"""

    minimum_dates_count = 2
    maximum_dates_count = 2

    # Array of events name (opens, closes etc)
    event_pretty_names = None

    def __init__(self):
        raise Exception('Unimplemented')

    def is_activity():
        return False

    def is_user_defined():
        return False

    def get_key():
        """"Return the letter of the planning key
        Q for Quiz, etc.
        Must be implemented by subclasses
        """
        raise Exception('Unimplemented')

    def get_pretty_name(self):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def get_start_datetime(self):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def get_start_timestamp(self):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def get_end_datetime(self):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def get_end_timestamp(self):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def set_start_datetime(self, datetime):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def set_end_datetime(self, datetime):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def get_timestamp_at_index(self, index):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def _set_date_at_index(self, datetime, index):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')

    def _get_arrow_at_index(self, index):
        """To be implemented by subclasses"""
        raise Exception('Unimplemented')


class Exam(Event):

    event_pretty_names = [
        'starts',
        'ends'
    ]

    def __init__(self, event_id):
        self.rel_id = event_id
        self.start_arrow = arrow.get(0)
        self.end_arrow = arrow.get(0)

    def is_activity():
        return True

    def is_user_defined():
        return True

    def get_key():
        return 'E'

    def get_pretty_name(self):
        return 'Exam'

    def get_start_datetime(self):
        return self.start_arrow.datetime

    def get_start_timestamp(self):
        return self.start_arrow.timestamp

    def get_end_datetime(self):
        return self.end_arrow.datetime

    def get_end_timestamp(self):
        return self.end_arrow.timestamp

    def set_start_datetime(self, datetime):
        self._set_date_at_index(datetime, 0)

    def set_end_datetime(self, datetime):
        self._set_date_at_index(datetime, 1)

    def get_timestamp_at_index(self, index):
        return self._get_arrow_at_index(index).timestamp

    def _set_date_at_index(self, datetime, index):
        if index == 0:
            self.start_arrow = arrow.get(datetime)
        elif index == 1:
            self.end_arrow = arrow.get(datetime)
        else:
            # TODO better err msg
            raise InvalidSyntaxException('Exam has invalid date count')

    def _get_arrow_at_index(self, index):
        if index == 0:
            return self.start_arrow
        elif index == 1:
            return self.end_arrow
        else:
            # TODO better err msg
            raise InvalidSyntaxException('Exam has invalid date count')


class CAPException(Exception):
    def __init__(self, alert, status):
        data = json.dumps({'alerts': [alert]})
        res = Response(data, status, mimetype='application/json')
        self.res = res
