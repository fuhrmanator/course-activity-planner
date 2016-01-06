#!/usr/bin/env python3
import os


class MoodleCourse():
    """Describes a complete moodle course from an archive on the disk"""
    def __init__(self, moodle_archive_path):
        self.path = moodle_archive_path
        self.activities_path = os.path.join(self.path, 'activities')

        if not os.path.isdir(self.activities_path):
            raise Exception('Invalid directory')

    def get_quizes(self):
        activities = os.listdir(self.activities_path)
        return [f for f in activities if f.startswith('quiz')]


def main():
    pass

if __name__ == "__main__":
    main()
