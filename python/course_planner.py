#!/usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET

from ics import Calendar as iCalendar


class GenericMeeting():
    def __init__(self, calendar_event):
        self.calendar_event = calendar_event


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


class Event():
    def __init__(self, path):
        self.activity = ET.parse(os.path.join(path, 'quiz.xml'))

        if len(self.activity.getroot()) != 1:
            raise Exception('An activity can only have one quiz.')
        self.quiz = self.activity.getroot()[0]

    def __getitem__(self, k):
        if k == 'id':
            return self.quiz.attrib[k]
        return self.quiz.find(k).text

    def __setitem__(self, k, v):
        if k == 'id' and 'id' in self.quiz.attrib:
            self.quiz.attrib[k] = v
        self.quiz.find(k).text = v

    def write(self, path):
        self.activity.write(path, short_empty_elements=False, encoding='UTF-8',
                            xml_declaration=True)


class MoodleQuiz():
    """Describes an XML Moodle quiz with key based access"""
    def __init__(self, path):
        self.activity = ET.parse(os.path.join(path, 'quiz.xml'))

        if len(self.activity.getroot()) != 1:
            raise Exception('An activity can only have one quiz.')
        self.quiz = self.activity.getroot()[0]

    def __getitem__(self, k):
        if k == 'id':
            return self.quiz.attrib[k]
        return self.quiz.find(k).text

    def __setitem__(self, k, v):
        if k == 'id' and 'id' in self.quiz.attrib:
            self.quiz.attrib[k] = v
        self.quiz.find(k).text = v

    def write(self, path):
        self.activity.write(path, short_empty_elements=False, encoding='UTF-8',
                            xml_declaration=True)


class MoodleCourse():
    """\
    Describes a complete Moodle course from an unpacked archive on the disk"""
    def __init__(self, moodle_archive_path):
        self.path = moodle_archive_path
        self.activities_path = os.path.join(self.path, 'activities')

        if not os.path.isdir(self.activities_path):
            raise Exception('Invalid directory')

    def get_quizzes(self):
        activities = os.listdir(self.activities_path)
        return [f for f in activities if f.startswith('quiz')]

    def get_quiz_by_module_id(self, module_id):
        """Gets a quiz from its module ID"""
        quizzes = self.get_quizzes()

        for quiz_path in quizzes:
            if quiz_path == 'quiz_%s' % module_id:
                return MoodleQuiz(os.path.join(self.activities_path, quiz_path))


def main():
    pass

if __name__ == "__main__":
    main()
