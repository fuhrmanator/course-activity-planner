<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Problem description](#problem-description)
  - [Course planning](#course-planning)
  - [Determining specific dates of activities](#determining-specific-dates-of-activities)
  - [Defining activities in separate systems](#defining-activities-in-separate-systems)
  - [Same dates go into various systems](#same-dates-go-into-various-systems)
  - [Lack of integration in legacy systems](#lack-of-integration-in-legacy-systems)
  - [Too much clicking!](#too-much-clicking)
  - [Grades must be synchronized across systems](#grades-must-be-synchronized-across-systems)
- [Instructor workflow](#instructor-workflow)
  - [Instructor updates dates for entire course at start of new semester](#instructor-updates-dates-for-entire-course-at-start-of-new-semester)
  - [Instructor updates details of an assignment before start of semester](#instructor-updates-details-of-an-assignment-before-start-of-semester)
  - [Instructor synchronizes grading data to SIGNETS](#instructor-synchronizes-grading-data-to-signets)
- [Concept of dates relative to meetings](#concept-of-dates-relative-to-meetings)
- [User stories](#user-stories)
- [Use cases](#use-cases)
  - [Manage course activities](#manage-course-activities)
  - [Plan section](#plan-section)
  - [Manage study groups](#manage-study-groups)
  - [Manage grade synchronization](#manage-grade-synchronization)
  - [Synchronize grades](#synchronize-grades)
- [Domain model](#domain-model)
- [Glossary](#glossary)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Problem description

The information here is still being incorporated from [this Google Document (originally in French, and visible only to people within ETSMTL.NET domain for now)](https://docs.google.com/a/etsmtl.net/document/d/1kHylinKFGfJcrfo8eo-BnmsEkC-JRSLPb2CYKz3oRLY/edit?usp=sharing).


This project fills a void between various online tools used by instructors in the execution of their teaching activities. We’ll use the situation at the ETS as an example, but probably there are analogous tools at other universities with similar problems:

 - PlanETS is the in-house Syllabus Management System (SMS), which aims to standardize the content of syllabi at the university.
 - SIGNETS is the in-house Grade Management System (GMS), which aims to standardize and facilitate the management of grades across all courses at the university.
 - Moodle is the Learning Management System (LMS), which aims to standardize the presentation of course content and provide instructors with pedagogical tools. 
 - The Course Calendar System is an abstraction of the various sources of data representing course calendars at ETS (it’s not really a system per se). This includes PDF files, iCal files, data available within PlanETS, etc.

## Course planning

A typical course contains several activities: homework assignments, quizzes, a mid-term exam and a final exam. Planning these activities requires specifying their dates: 

 1. every week there is a reading quiz at the start of a each class session, covering reading material that was to be read since the previous class session;
 2. at week 6 there is a mid-term;
 3. at weeks 4 and 8 there are homeworks assignments to turn in;
 4. at weeks 3, 6, 9 and 13 there are laboratory reports to turn in before each laboratory session;
 5. etc.
This planning applies every time the instructor teaches the course. 

Using online tools to manage these activities requires specifying precise dates of the activities. Unfortunately there is no tool that helps an instructor with determining these dates. Here are the challenges that an instructor faces:

 - **Meeting dates and times for the section of a course depend on its schedule and the university calendar.** For example, a section of a course could have seminar meetings on Wednesday from 1:30pm-5pm and laboratory meetings on Friday from 8:30am-10:30am. The ninth Wednesday of the semester could be a holiday, so the seminar would not be held on that day. The ninth Tuesday of the semester could be permutated to a Wednesday (meaning the seminar should meet exceptionally on that day). These dates are available through SIGNETS in its user interface, but there is no way to export the information as a calendar. Furthermore, this data isn’t typically available until the rooms for the meeting activities have been determined, which can sometimes occur 3 weeks before a semester starts. Instructors need to plan much earlier.

 - **Dates and times of activities (quizzes, exams, homeworks, etc.) must be adjusted to the meeting dates as above.** For example, each reading quiz should be opened in Moodle at the end of one lecture meeting and it should close in Moodle 30 minutes prior to the next meeting. Instructors must determine the dates/times manually. No tools exist to aid in this step.
 - **SIGNETS, PlanETS and Moodle all have different human-machine interfaces to specify metadata for the activities (their value, weight, dates, etc.), and the metadata for the same activities must be defined by the instructor in each system.** For a one section of a course with 20 activities (LOG210 is an example), it is a very long process that involves much clicking (more than 500 clicks) and is error-prone. In many cases, instructors don’t modify the dates in SIGNETS, because the whole process takes too long. 

 - **Grades for activities evaluated in Moodle must be imported into SIGNETS.** Although there exists an import function, it is complex and error-prone when there are many activities. For example, transferring reading quizzes and homeworks from Moodle to SIGNETS in LOG210 requires exporting the data from Moodle to an Excel file on a PC, then importing the Excel file into SIGNETS. The instructor is required to match up the names of the activities in SIGNETS to the names of the activities in Moodle. If no errors occur, it’s a process that takes 15 minutes. Typical errors are things such as inconsistent metadata between SIGNETS and Moodle, e.g., Homework 1 was graded in Moodle on a scale of 100, but it was defined in SIGNETS on a scale of 10. Such errors cause the import to fail and the instructor must go back and redefine the metadata in SIGNETS for the Homework 1 so that it is on a scale of 100 as in Moodle. Because this process is complex, instructors wait until the end of the semester to do it. This means that SIGNETS has less value to the students during the semester when Moodle is used (they must look in SIGNETS for some grades such as the mid-term, and in Moodle for homework and quiz grades). 

## Determining specific dates of activities
The problem is that the tools must be configured with **specific dates** for these activities. For example, the mid-term at week 6 could have a specific date of 2015-06-03 because the section’s classes meet on Wednesdays. Another section of the same course that has classes on Friday would have its week 6 mid-term on 2015-06-05 (two days later). 

The specific dates are not just a function of what day of the week (and time of day) the class or laboratory meets. The university’s course calendar provides information that complicates determining a specific date. The calendar contains university holidays, breaks and (at ETS) day permutations (on a given day the courses are given as if it were another day of the week, i.e., a given Wednesday follows a schedule as if it were a Thursday). 

The following diagram shows a real example for a course section 01 of LOG210 from the summer trimester 2015 at ETS. The Quebec National Day and Canada Day fall on the same days as the section seminar (Wednesdays). There can therefore be no seminar on those two days. However, the university plans a day permutation on Tuesday 2015-06-23 to allow Wednesday events. Note that this also means Tuesday courses on that day would not take place. In this example we see that the Friday laboratory sessions are not affected. 

![Calendar showing holidays and day permutation](https://cloud.githubusercontent.com/assets/7606540/10250670/44c8e1b2-68fa-11e5-84b3-53c416015160.png)

So when an ETS instructor who is responsible for the syllabus for LOG210 that is offered in 3 sections in the summer wants to specify the three mid-term dates, she has to be very careful to layout the calendar and be precise about which days are the week 6 for each of the sections.

Without this kind of calendar view, it can be complicated for the instructor to determine the exact date of week 6’s mid-term. If she’s teaching more than one section of the course in the same semester, then week 6 is likely not the same day in each section. 

## Defining activities in separate systems
If instructors want to use an LMS to do the quizzes and homeworks online, those activities must be created in the LMS. If those activities are graded, then the GMS has to also be updated with those activities. In both the LMS and GMS, activities have specific dates in their specifications.

Consider determining the dates for the weekly quizzes and other homeworks when they are done online through the LMS. Before the use of online-systems, instructors specified due dates in class or on the web site. However, using the LMS means instructors have to specify the date in the assignment or quiz. Quizzes, in particular, can be very effective if the LMS turns off the access to them say 30 minutes before the course begins. This encourages students to do required readings. In this case, it’s not just a date, but also a time. If one course begins at 9am, then the instructor has to specify a closing date for each quiz that is 8:30am for every day there is a quiz. In an LMS such as Moodle (or Sakai), setting the dates for a quiz involves a lot of clicking (in Moodle it can be as many as 20 clicks to set the dates and times for one quiz). In a course that has 10+ quizzes and several homeworks, it’s approaching 500 clicks to set up the LMS for one section of the course. If there are multiple sections, the instructor has that same number of clicks for each section, because sections occur at different times. Moodle, for example, offers no help in making this process easier.

## Same dates go into various systems
Dates for anything that gets a grade will also need to be put into the GMS (SIGNETS et ETS). Instructors can copy the grade structure in SIGNETS from another section of the course, but the dates are not reset automatically for the new section. Again, it’s at least 10 clicks to set a date for a graded activity in SIGNETS, and there are about 20 activities in my LOG210 course, resulting in a lot of clicking inside the GMS to set up one section of a course. This gets repeated for every section.

## Lack of integration in legacy systems
The problem that exists is due to redundant information on activities across several legacy systems that aren't integrated, as shown in the following diagram:

![Lack of integration across legacy systems](http://plantuml.com/plantuml/svg/3Sp13S8m3030LM20ndysGEB12gvh4ak97JasgDlJr_tkBaez3qxljnOnrmF0yLUgHCiz5pkP1ciKiW6VR3vGCSo1B7tnXXJobJYtsL6L7GQkk3330rvSaSxd5LJ74DEtszvvb9cZ_m40)

## Too much clicking!
All that clicking is boring and prone to human error. For example, in Moodle, to set the open date of a quiz, one must choose the day, the month, the year, the hour and the minutes, each from separate drop-down menus on a web page. After 20 minutes of this kind of brain-numbing clicking, it’s very easy to make a mistake in one of these choices.

## Grades must be synchronized across systems
When students complete online quizzes or assignments, the grades are stored in the LMS. However, those grades need to show up ultimately in the university’s GMS (not all courses are using the LMS). The SIGNETS system at ETS has some functions to import grades from Moodle, but the process is tedious and requires precise configuring of the activities in both systems to work properly. The process involves a lot of manual steps (exporting data from Moodle in the correct format to a PC hard drive, signing into SIGNETS and choosing the import function, matching the data up, etc.). It’s at least 15 minutes work if there are no glitches, but this is rare. For example, activity names in Moodle (when exported) have the word “Assignment:” or “Quiz:” added to the beginning, making them too long for the names of activities in SIGNETS. This means SIGNETS can’t determine the match of the data and the instructor has to match them up manually during the import step. If an activity is defined in the GMS as being graded on a scale of 10 points, but in Moodle it was graded on a scale of 20 points, the data fail to import (rightly so). This means that if an instructor changes the details of an activity in one system, she must make the changes consistent across all the systems. It can take more than an hour to do the transfer when there are these kinds of problems.

For these reasons, instructors wait until the end of the semester to perform synchronization. Ideally, students would see their grades inside the GMS shortly after they complete a quiz or get an assignment grade in the LMS (rather than waiting until the end of the semester when a manual synchronization occurs). 

# Instructor workflow
The following diagrams document a way for an instructor to manually configure these systems. They are based on the experience of C. Fuhrman. Other points of view about ways to use these systems should be solicited.

## Instructor updates dates for entire course at start of new semester

![Instructor updates dates for entire course at start of new semester](http://plantuml.com/plantuml/svg/BOan3i8m302_0WzelBDLOcJb0IPncqYE7JasgB-dGuVJINVt9fcZK1ZVglkO3m33NzgRr_Z49CigJk8fQuSjgdKKT3N86ZPfmUpjs_nO1gC86NISVaeL2wpNV8-2Ji-JkJ9VjT5yqOxvI2Cw_m40.svg)

## Instructor updates details of an assignment before start of semester
![Instructor updates details of one activity before start of semester](http://plantuml.com/plantuml/svg/DSan3i8m343Hgy016kziI8oLEd40uvWcKc97ZWtgxM60wKlldwjGYynXxLJSnxm06BxJNht48oORgJYB9z8EpoZMKT3LW3HiyeBazLNzM4P34JReEFqRLSnm_StxoEXyOyVQvYRyzvLtf2EDwEq3.svg)

## Instructor synchronizes grading data to SIGNETS

![instructor synchronizes grades](http://plantuml.com/plantuml/svg/BSan4W8n2030h-W3BlHsLZPslW09TybC0Xa2El7rMbXjiUSgr29pM3iLzp4l08RlT5GlyOp9HYhEuecqmnx5EWgw6f26JTwGlBwghsqq5663ZjD_g6A6wpyVIwYOIltmpJ3plFE1jDA8thu0.svg)

# Concept of dates relative to meetings
It could be useful if activities could be defined with dates that are relative to a particular meeting. Here are a few examples:

![Course meetings and activities that take place relative to them](http://plantuml.com/plantuml/svg/7SlB3G8n303HLg20ZUzSeG8wC5v38Zbsv0-8xbbnciFJd8UIrCxbSkgPAou0Zf_s6jdhKS5EficQZMp2ixfFL4np82iFtf1ol4T-joMeoWuJ8u-OuGvt5ZoORvWSr_yGRTMK7m00)

![Lab meetings and activities that take place relative to them](http://plantuml.com/plantuml/svg/3Scx4S8m303GLM20M3qr9HKRA8h0lfCbdpvmR4-gLxphK98wk5mkFNF53S3nszuZU-qLx6IQhDd89hog-qJ5D0Uoyk0DASTdv6zRWghiC37on0mFUBBWsNp7v7ZW7ctLb3y0)

# User stories

We're trying to track these as issues:
 - [#1](../../../issues/1)

 - As an instructor, I want to plan my activities in one place, because I don't want to repeat myself when entering information. 

 - As an instructor, I want to reuse the planning of activities from another section of a course, because I don't want to waste time re-defining the same information.


# Use cases
![Use case diagram in PlantUML](http://www.plantuml.com/plantuml/svg/3SlB3OCm303GLUW0YUziunf38YLsv0zLjuVJExrF5nfvSDhOMiJo7S3mLwyUBR_fRAGIB5599vpPRA9Wg05fcdD1Ydxt-9SrK8GD9dgygE81xo-4pbvNpl40.svg)

## Manage course activities
Instructors add/delete/modify course activities for a course. This includes importing existing activities defined in the LMS and GMS. These activities represent a general structure to the course as well as their grading details and weight. For example, instructors define the number of exams, quizzes, homeworks, etc., as well as their timing within the course, e.g., 
 - exam 1 is worth 20% and occurs during the 6th lecture session, 
 - reading quiz 2 is worth 1% and is available on the LMS immediately after the 1st lecture session and has a deadline of 30 minutes before the 2nd lecture session 4, 
 - etc. 

## Plan section
Instructors need to configure dates for course activities that are relative to a course section’s calendar. Those dates must be pushed to the various related systems: LMS, GMS and Syllabus. 

## Manage study groups
The GMS (SIGNETS) offers tools to create study groups. An instructor can ask the tool to create teams of *N* students for working on group activities. Team creation can be done with various algorithms (random, according to GPA, specified by the instructor, etc.). Team activities that involve the LMS (Moodle) require that the team information created in the GMS (SIGNETS) be synchronized with the LMS (Moodle). This use case attempts to manage the way this is done.

## Manage grade synchronization
As activities that are done within the LMS are graded, synchronization is necessary between the LMS and the GMS. Instructors can configure if this is done and how frequently it should occur.

## Synchronize grades
Synchronization between LMS and GMS occurs according to how it is configured. 


# Domain model
![Domain model in PlantUML](http://plantuml.com:80/plantuml/svg/3SNB4K8n2030LhI0XBlTy0YQpF394D2nUztBtfUHrE0AkStCVHu0WP_-MZdhgiD1RicMdLpXMJCK3TC3o2iEDwHSxvNVjWNDE43nv3zt731SSLbJ7onzbyeF)

# Glossary

Term | Definition | Synonyms
---- | ---------- | --------
Course | a unit of study in a subject area identified by a description of activities |
Activity | an interaction that students have with the instructor (e.g., attending a lecture session, taking a mid-term exam), a teaching assistant (e.g., writing a laboratory report), other students (e.g., submitting a homework for peer evaluation), or a LMS (e.g., taking an online multiple-choice quiz), all of which may receive a grade. |
Section | a group of one or more students registered to take a course together and assigned to be under the general direction of a particular instructor, with a particular schedule. | Français : *groupe-cours*
Instructor | | Professor, teaching assistant, grader, lab assistant
Syllabus | an outline of the subjects in a course, but in many institution it also specifies dates, values and types of graded activities, as well as how the final grade is calculated. |
Grade | an evaluation of an activity, which may be recorded in the grade management system.
Grade Management System | an online system that records grades of individual activities, often developed by the university, separate from the LMS.
Session Calendar | the dates for the individual sessions of a course section, including the various types of meetings, e.g., seminars every Monday from 9am-12pm, laboratory sessions every Wednesday 10am-12pm 
Session | periods of time, typically on a fixed weekly schedule, where some activities take place, e.g., lecture course, seminar, colloquium, tutorial, laboratory, etc. | Meeting
Term Calendar | the dates, determined by the institution, for the start and end of a term, as well as holidays, breaks or day permutations.
Holiday | a day of festivity or recreation when no sessions are held, specified in the term calendar.
Break | a period of time during a term when no sessions are held, e.g., spring break, Easter break, etc., specified in the term calendar.
Day Permutation | a special change indicated in a term calendar where sessions that normally occur on one day are changed to another, e.g., on a specific Tuesday during the term, sessions are given as if it were a Monday (a technique used in some institutions to recover sessions lost by holidays or breaks).
Term | a portion of an academic year, the time during which an educational institution holds classes. The schedules adopted vary widely. https://en.wikipedia.org/wiki/Academic_term 
Schedule | a table for coordinating these elements: Students, Instructors, Rooms, Sessions https://en.wikipedia.org/wiki/School_timetable | Timetable
