#!/usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET

from ics import Calendar as iCalendar


class GenericMeeting():
    def __init__(self, calendar_event):
        self.calendar_event = calendar_event


class Quiz(GenericMeeting):
    def __init__(self, *args, **kwargs):
        GenericMeeting.__init__(self, *args, **kwargs)


class Seminar(GenericMeeting):
    def __init__(self, *args, **kwargs):
        GenericMeeting.__init__(self, *args, **kwargs)


class Practica(GenericMeeting):
    def __init__(self, *args, **kwargs):
        GenericMeeting.__init__(self, *args, **kwargs)


class CalendarReader():
    """Reads iCalendar and returns generic meetings"""

    # Association of the meeting classes and their regex in the calendar
    candidates = {Seminar: re.compile(r'Cours magistral ([0-9]{1,2})$'),
                  Practica: re.compile(r'TP ([0-9]{1,2})$')}

    def __init__(self, calendar_path):
        with open(calendar_path, 'r') as cal_file:
            cal_content = cal_file.readlines()
            self.calendar = iCalendar(cal_content)

    def get_all_meetings(self):
        """Parses events from calendar and orders them by meeting type.
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


class MoodleEvent():
    """Describes an XML Moodle event with key based access"""
    def __init__(self, path):
        self.activity = ET.parse(path)

        if len(self.activity.getroot()) != 1:
            raise Exception('An activity can only have one event.')
        self.event = self.activity.getroot()[0]

    def __getitem__(self, k):
        if k == 'id':
            return self.event.attrib[k]
        return self.event.find(k).text

    def __setitem__(self, k, v):
        if k == 'id' and 'id' in self.event.attrib:
            self.event.attrib[k] = v
        self.event.find(k).text = v

    # def write(self, path):
    #   self.activity.write(path, short_empty_elements=False, encoding='UTF-8',
    #                         xml_declaration=True)


class MoodleQuiz(MoodleEvent):
    """Describes an XML Moodle quiz with key based access"""
    def __init__(self, path):
        super().__init__(os.path.join(path, 'quiz.xml'))


class MoodleAcivityIndex():
    def __init__(self, module_id, section_id, module_name, directory):
        self.module_id = module_id
        self.section_id = section_id
        self.module_name = module_name
        self.directory = directory


class MoodleCourse():
    """\
    Describes a complete Moodle course from an unpacked archive on the disk"""

    modname_to_class = {'quiz': MoodleQuiz}

    def __init__(self, moodle_archive_path):
        self.path = moodle_archive_path
        self.activities = {}
        self.activities_seq = {}
        for clazz in self.modname_to_class.values():
            self.activities[clazz] = []

        self.fullpath = os.path.join(self.path, 'moodle_backup.xml')
        self.backup = ET.parse(self.fullpath)

        self._load_activities_and_section_order()

    def _load_section_order(self):
        """"Read the activity sequence from sections.xml.
        Returns a list of the module_ids in order of the course.
        """
        section_dir = self.backup.getroot().find('information'). \
            find('contents').find('sections')[0].find('directory').text

        section_path = os.path.join(self.path, section_dir, 'section.xml')

        section = ET.parse(section_path).getroot()
        return [int(num) for num in section.find('sequence').text.split(',')]

    def _load_activities_and_section_order(self):
        section_order = self._load_section_order()

        for a in self.backup.getroot().find('information').find('contents'). \
                find('activities'):
            module_name = a.find('modulename').text
            directory = a.find('directory').text

            if module_name not in self.modname_to_class:
                print('ignoring ', module_name)
                continue

            clazz = self.modname_to_class[module_name]
            self.activities[clazz].append(
                clazz(os.path.join(self.path, directory)))

        if len(self.backup.getroot().find('information').find('contents').
                find('sections')) > 1:
            raise Exception('Not implemented')

    def get_quiz_by_relative_num(self, number):
        return self.quizzes[number - 1]

    # def get_quiz_by_module_id(self, module_id):
    #     for quiz in self.quizzes:
    #         if quiz['id'] == module_id:
    #             return quiz

    def load_quiz_from_xml(self, xml):
        pass

    def _load_quizzes(self):
        quizzes = []
        for quiz_path in self._get_quizzes():
            quizzes.append(
                MoodleQuiz(os.path.join(self.activities_path, quiz_path)))


def main():
    pass

if __name__ == "__main__":
    main()
