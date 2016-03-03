class Event():
    """Abstract class to be extended with all event (activity or meeting)"""

    def __init__(self, arg):
        raise Exception('Unimplemented')

    def is_activity():
        return False

    def get_key(self):
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
