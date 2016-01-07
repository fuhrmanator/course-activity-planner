#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET


class MoodleQuiz():
    """Describes a MoodleQuiz with basic information"""
    def __init__(self, path):
        self.activity = ET.parse(os.path.join(path, 'quiz.xml'))

        if len(self.activity.getroot()) != 1:
            raise Exception('An activity can only have one quiz.')
        self.quiz = self.activity.getroot()[0]

    def __getitem__(self, k):
        if k == 'id':
            return self.quiz.attrib[k]
        return self.quiz.find(k).text

    def write(self, path):
        self.activity.write(path, short_empty_elements=False, encoding='UTF-8',
                            xml_declaration=True)


class MoodleCourse():
    """Describes a complete moodle course from an archive on the disk"""
    def __init__(self, moodle_archive_path):
        self.path = moodle_archive_path
        self.activities_path = os.path.join(self.path, 'activities')

        if not os.path.isdir(self.activities_path):
            raise Exception('Invalid directory')

    def get_quizzes(self):
        activities = os.listdir(self.activities_path)
        return [f for f in activities if f.startswith('quiz')]

    def get_quiz_by_module_id(self, module_id):
        """Gets a quiz from it's ID"""
        quizzes = self.get_quizzes()

        for quiz_path in quizzes:
            if quiz_path == 'quiz_%s' % module_id:
                return MoodleQuiz(os.path.join(self.activities_path, quiz_path))


def main():
    pass

if __name__ == "__main__":
    main()
