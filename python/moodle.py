import os
import arrow
import tarfile
import xml.etree.ElementTree as ET

from dateutil import tz
from common import Event


class MoodleActivity(Event):
    """Describes an XML Moodle event with key based access"""

    event_keys = [
        'timeopen',
        'timeclose'
    ]
    # for preview
    event_pretty_names = [
        'opens',
        'closes'
    ]

    minimum_dates_count = 2
    maximum_dates_count = 2

    def __init__(self, path):
        self.modified = False
        self.path = path
        self.tree = ET.parse(path)
        self.activity = self.tree.getroot()

        if len(self.activity) != 1:
            raise Exception('An activity can only have one event.')
        self.event = self.activity[0]

    def __getitem__(self, k):
        if k == 'id':
            return self.event.attrib[k]
        if k == 'moduleid':
            return int(self.activity.attrib[k])
        return self.event.find(k).text

    def __setitem__(self, k, v):
        if k == 'id' or k == 'moduleid':
            raise Exception('Not allowed')
        self.event.find(k).text = v
        self.modified = True

    def is_activity():
        return True

    def set_start_datetime(self, datetime):
        self._set_date_at_index(datetime, 0)

    def set_end_datetime(self, datetime):
        self._set_date_at_index(datetime, 1)

    def get_start_datetime(self):
        return self._get_arrow_at_index(0).datetime

    def get_start_timestamp(self):
        return self._get_arrow_at_index(0).timestamp

    def get_end_datetime(self):
        return self._get_arrow_at_index(1).datetime

    def get_end_timestamp(self):
        return self._get_arrow_at_index(1).timestamp

    def get_title(self):
        return self.__getitem__('name')

    def write(self):
        if not self.modified:
            return
        self.tree.write(self.path, short_empty_elements=False, encoding='UTF-8',
                        xml_declaration=True)
        self._write_calendar()

    def _write_calendar(self):
        moodle_cal_path = os.path.join(self.global_path, 'calendar.xml')
        cal_tree = ET.parse(moodle_cal_path)
        events = cal_tree.getroot()

        if len(events) > 2 or len(events) < 1:
            raise Exception('Unimplemented')

        events[0].find('timestart').text = str(self.get_start_timestamp())
        events[0].find('timeduration').text = 0

        if len(events) > 1:
            events[0].find('timeduration').text = str(
                self.get_end_timestamp() - self.get_start_timestamp())

            events[1].find('timeduration').text = 0
            events[1].find('timestart').text = str(self.get_end_timestamp())

        cal_tree.write(moodle_cal_path, short_empty_elements=False,
                       encoding='UTF-8', xml_declaration=True)

    def _set_date_at_index(self, datetime, index):
        k = self.event_keys[index]
        timestamp = str(arrow.get(datetime).to('utc').timestamp)
        self.__setitem__(k, timestamp)

    def _get_datetime_at_index(self, index):
        return self._get_arrow_at_index(index).datetime

    def _get_timestamp_at_index(self, index):
        return self._get_arrow_at_index(index).timestamp

    def _get_start_arrow(self):
        """Returns end as arrow object"""
        return self._get_arrow_at_index(0)

    def _get_end_arrow(self):
        """Returns end as arrow object"""
        return self._get_arrow_at_index(1)

    def _get_arrow_at_index(self, index):
        """Gets the arrow object representation of the start or close event.
        """
        k = self.event_keys[index]
        epoch = self.event.find(k).text
        return arrow.get(epoch, tzinfo=tz.gettz('America/Montreal'))


class MoodleQuiz(MoodleActivity):
    """Describes an XML Moodle quiz with key based access"""

    def __init__(self, path):
        self.global_path = path
        super().__init__(os.path.join(path, 'quiz.xml'))

    def get_pretty_name(self):
        return 'Quiz'

    def get_key(self):
        return 'Q'


class MoodleChoice(MoodleActivity):
    """Describes an XML Moodle choice with key based access"""

    def __init__(self, path):
        self.global_path = path
        super().__init__(os.path.join(path, 'choice.xml'))

    def get_pretty_name(self):
        return 'Choice'

    def get_key(self):
        return 'C'


class MoodleFeedback(MoodleActivity):
    """Describes an XML Moodle feedback with key based access"""

    def __init__(self, path):
        self.global_path = path
        super().__init__(os.path.join(path, 'feedback.xml'))

    def get_pretty_name(self):
        return 'Feedback'

    def get_key(self):
        return 'F'


class MoodleLesson(MoodleActivity):
    """Describes an XML Moodle lesson with key based access"""

    event_keys = [
        'available',
        'deadline'
    ]
    # for preview
    event_pretty_names = [
        'opens',
        'closes'
    ]

    def __init__(self, path):
        self.global_path = path
        super().__init__(os.path.join(path, 'lesson.xml'))

    def get_pretty_name(self):
        return 'Lesson'

    def get_key(self):
        return 'L'


class MoodleHomework(MoodleActivity):
    """Describes an XML Moodle assignment (homework) with key based access"""
    maximum_dates_count = 3

    event_keys = [
        'allowsubmissionsfromdate',
        'duedate',
        'cutoffdate',
    ]

    # for preview
    event_pretty_names = [
        'opens',
        'is due',
        'closes'
    ]

    def __init__(self, path):
        self.global_path = path
        super().__init__(os.path.join(path, 'assign.xml'))

    def get_pretty_name(self):
        return 'Homework'

    def get_key(self):
        return 'H'

    def _write_calendar(self):
        moodle_cal_path = os.path.join(self.global_path, 'calendar.xml')
        cal_tree = ET.parse(moodle_cal_path)
        events = cal_tree.getroot()

        if len(events) != 1:
            raise Exception('Unimplemented')

        events[0].find('timestart').text = str(self.get_end_timestamp())
        events[0].find('timeduration').text = 0

        cal_tree.write(moodle_cal_path, short_empty_elements=False,
                       encoding='UTF-8', xml_declaration=True)


class MoodleCourse():
    """\
    Describes a complete Moodle course from an unpacked archive on the disk"""

    modname_to_class = {
        'quiz': MoodleQuiz,
        'assign': MoodleHomework,
        'feedback': MoodleFeedback,
        'lesson': MoodleLesson,
        'choice': MoodleChoice
        }

    def __init__(self, moodle_archive_path):
        self.path = moodle_archive_path
        self.fullpath = os.path.join(self.path, 'moodle_backup.xml')
        self.backup = ET.parse(self.fullpath)

        self._load_activities_and_sequence()

    def replace_event(self, activity):
        self.activities[type(activity)][activity.rel_id - 1] = activity

    def get_activity_by_type_and_num(self, type, relative_number):
        return self.activities[type][relative_number - 1]

    def write(self, output_path):
        self._write_activities_to_disk()

        # Moodle archives require special care !
        # Archive must be created like this `tar -cf archive.mbz *`
        ogwd = os.getcwd()
        os.chdir(self.path)
        full_output_path = os.path.join(ogwd, output_path)

        with tarfile.open(full_output_path, "w:gz") as archive:
            for name in os.listdir(self.path):
                archive.add(name)
            archive.close()
        os.chdir(ogwd)

    def _load_activity_sequence(self):
        """"Read the activity sequence from moodle_backup.xml.
        Returns a list of the module_ids in order of the course.
        """
        o = []
        activities = self.backup.getroot().find('information') \
            .find('contents').find('activities')

        for activity in activities:
            o.append(int(activity.find('moduleid').text))
        return o

    def _load_activities_and_sequence(self):
        self.activity_sequence = self._load_activity_sequence()
        self.activities = self._load_activites()

    def _load_activites(self):
        activities = {}
        for clazz in self.modname_to_class.values():
            activities[clazz] = []

        for a in self.backup.getroot().find('information').find('contents'). \
                find('activities'):
            module_name = a.find('modulename').text
            directory = a.find('directory').text

            if module_name not in self.modname_to_class:
                continue  # Ignore incomptatible activity

            clazz = self.modname_to_class[module_name]
            activities[clazz].append(clazz(os.path.join(self.path, directory)))

        for activity_type, items in activities.items():
            activities[activity_type] = self._sort_activity_type(items)

        return activities

    def _sort_activity_type(self, activities):
        s = sorted(activities, key=lambda activity:
                   self.activity_sequence.index(activity['moduleid']))
        # Set relative id of activity
        for i, activity in enumerate(s):
            activity.rel_id = i + 1
        return s

    def _write_activities_to_disk(self):
        for activities in self.activities.values():
            for activity in activities:
                activity.write()
