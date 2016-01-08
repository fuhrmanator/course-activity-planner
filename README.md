<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [course-activity-planner](#course-activity-planner)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# course-activity-planner
Tool for instructors to plan course activities and synchronize the data with syllabus, LMS, etc.

### Setup
* Setup a python virtualenv
```
cd python && virtualenv env
```

### Run unit tests
* Activate the python virtualenv
```
. env/bin/activate
```
* Install the dependencies
```
pip install -r requirements.txt
```
* Run the test suite
```
nosetests *.py
```
* Optionally, you can get a coverage report
```
nosetests --with-cov --cov-report html --cov-config .coveragerc test.py
```
