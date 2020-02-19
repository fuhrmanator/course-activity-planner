import yaml
import glob

from common import UserDefinedEvent


class ActivityLoader():
    """Loads user defined activities from YAML config"""

    def __init__(self):
        self.activities = []

        for f in glob.glob('config/activities/*.yaml'):
            stream = open(f, 'r')
            yaml_data = yaml.load(stream, Loader=yaml.SafeLoader)
            self.activities.append(
                UserDefinedEvent(key=yaml_data['key'], name=yaml_data['name']))

    def get_activities_instances(self):
        return self.activities
