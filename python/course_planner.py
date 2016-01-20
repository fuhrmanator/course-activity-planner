#!/usr/bin/env python3
import tarfile
import tempfile
import shutil

from ics_calendar import CalendarReader
from moodle import MoodleCourse
from interpreter import Interpreter


def main():
    ics_file = '../ActivitETS/multi-fr.ics'
    mbz_file = '\
../backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz'
    relative_planning_file = 'planning.txt'

    # Setup calendar
    calendar = CalendarReader(ics_file)
    calendar_meetings = calendar.get_all_meetings()

    # Setup Moodle course
    tmp_path = tempfile.mkdtemp()
    with tarfile.open(mbz_file) as tar_file:
        tar_file.extractall(tmp_path)
    course = MoodleCourse(tmp_path)

    interpreter = Interpreter(calendar_meetings, course)

    with open(relative_planning_file, 'r') as f:
        for line in f:
            interpreter.get_new_event_from_string(line)

    course.write('test.mbz')
    shutil.rmtree(tmp_path)


if __name__ == "__main__":
    main()
