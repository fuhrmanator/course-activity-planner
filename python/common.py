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
    show_planets = False

    def __init__(self):
        raise Exception('Unimplemented')

    def is_activity(self=None):
        return False

    def is_user_defined(self=None):
        return False

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


class UserDefinedEvent(Event):
    """Basic partial implementation of a user defined
    event with only dates 'start' and 'end'
    """

    event_pretty_names = [
        'starts',
        'ends'
    ]

    def __init__(self, event_id=0, key=None, name=None, planets_name=None):
        self.rel_id = event_id
        self.key = key
        self.name = name
        self.planets_name = planets_name
        if planets_name:
            self.show_planets = True

    def is_activity(self=None):
        return True

    def is_user_defined(self=None):
        return True

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
            raise InvalidSyntaxException('Invalid date count')

    def _get_arrow_at_index(self, index):
        if index == 0:
            return self.start_arrow
        elif index == 1:
            return self.end_arrow
        else:
            # TODO better err msg
            raise InvalidSyntaxException('Invalid date count')


class CAPException(Exception):
    def __init__(self, alert, status):
        data = json.dumps({'alerts': [alert]})
        res = Response(data, status, mimetype='application/json')
        self.res = res
