from common import UserDefinedEvent


class ActivityLoader():
    """Loads user defined activities from YAML config"""

    def __init__(self):
        pass

    def get_activities_instances(self):
        return [
            UserDefinedEvent(key='E', name='Exam'),
            UserDefinedEvent(key='UQ', name='UserQuiz')]
