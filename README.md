<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [course-activity-planner](#course-activity-planner)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# course-activity-planner
Tool for instructors to plan course activities and synchronize the data with syllabus, LMS, etc.

### Run unit tests
* Copy the archive in the test-data folder:

`cp ActivitETS/backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz python/test-data/`
* Extract the contents of the archive in the test-data directory:

`cd python/test-data && tar -xf  test-data/backup-moodle2-course-1677-s20143-log792-09-20151102-1202-nu.mbz`
* Run the test suite:

`cd ../ && ./test.py`
