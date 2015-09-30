

# User stories

We're trying to track these as issues:
 - [#1](../../../issues/1)

From the original document (in French):

 - En tant qu’enseignant, je veux planifier les activités pédagogiques à un seul endroit, parce que je ne veux pas répéter la saisie des informations.

 - En tant qu’enseignant, je veux réutiliser la planification des activités pédagogiques d’un autre groupe-cours, parce que je ne veux pas répéter la saisie des informations.


# Use cases
![Use case model in PlantUML](http://www.plantuml.com/plantuml/svg/3SlB3OCm303GLUW0YUziunf38YLsv0zLjuVJExrF5nfvSDhOMiJo7S3mLwyUBR_fRAGIB5599vpPRA9Wg05fcdD1Ydxt-9SrK8GD9dgygE81xo-4pbvNpl40)

## Manage course activities
Instructors add/delete/modify course activities for a course. This includes importing existing activities defined in the LMS and GMS. These activities represent a general structure to the course as well as their grading details and weight. For example, instructors define the number of exams, quizzes, homeworks, etc., as well as their timing within the course, e.g., 
 - exam 1 is worth 20% and occurs during the 6th lecture session, 
 - reading quiz 2 is worth 1% and is available on the LMS immediately after the 1st lecture session and has a deadline of 30 minutes before the 2nd lecture session 4, 
 - etc. 

## Plan section
Instructors need to configure dates for course activities that are relative to a course section’s calendar. Those dates must be pushed to the various related systems: LMS, GMS and Syllabus. 
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
