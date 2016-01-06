#!/usr/bin/env python3
import os


def get_quizes(moodle_archive_path):
    moodle_activities_path = os.path.join(moodle_archive_path, 'activities')
    if not os.path.isdir(moodle_activities_path):
        print('Invalid directory')
        exit(1)

    activities = os.listdir(moodle_activities_path)

    return [f for f in activities if f.startswith('quiz')]


def main():
    pass

if __name__ == "__main__":
    main()
