# LMS interfacing
Interfacing with the LMS could be done in various ways:
 - REST API, e.g., http://stackoverflow.com/q/19903456/1168342 or http://stackoverflow.com/questions/24730583/create-quiz-using-rest-api-in-moodle
 - via files that are imported/exported
 
In the case of Moodle (the LMS at ÉTS), the shortest-term solution might be to use the backup file.

# Format of a Moodle Backup file
It's a file of type `.mbz` which can be opened using 7-Zip (Windows). It contains directories, some of which contain information about activities (quizzes, assignments, etc.).

![screenshot of Moodle .mbz file inside 7-zip in Windows](https://cloud.githubusercontent.com/assets/7606540/10108355/6fb03536-638e-11e5-8ac0-1ee69b15e009.png)

For example:
    `backup-moodle2-course-2558-s20152-log210-01-20150609-1748-nu.mbz\backup-moodle2-course-2558-s20152-log210-01-20150609-1748-nu\activities\quiz_108660\` 
    
This represents a single quiz. In the directory are several XML files, notably `quiz.xml` which contains data about dates, notably the `<timeopen>` and `<timeclose>` elements:
 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<activity id="2970" moduleid="108660" modulename="quiz" contextid="150719">
  <quiz id="2970">
	<name>Mini test semaine 1</name>
	<intro></intro>
	<introformat>1</introformat>
	<timeopen>1430341200</timeopen>
	<timeclose>1430931600</timeclose>
	<timelimit>900</timelimit>
	<overduehandling>autosubmit</overduehandling>
	<graceperiod>0</graceperiod>
	<preferredbehaviour>immediatefeedback</preferredbehaviour>
	<attempts_number>3</attempts_number>
	<attemptonlast>0</attemptonlast>
	<grademethod>1</grademethod>
	<decimalpoints>2</decimalpoints>
	<questiondecimalpoints>-1</questiondecimalpoints>
	<reviewattempt>69904</reviewattempt>
	<reviewcorrectness>69904</reviewcorrectness>
	<reviewmarks>69904</reviewmarks>
	<reviewspecificfeedback>69904</reviewspecificfeedback>
	<reviewgeneralfeedback>16</reviewgeneralfeedback>
	<reviewrightanswer>0</reviewrightanswer>
	<reviewoverallfeedback>0</reviewoverallfeedback>
	<questionsperpage>1</questionsperpage>
	<navmethod>free</navmethod>
	<shufflequestions>0</shufflequestions>
	<shuffleanswers>1</shuffleanswers>
```

Moodle's documentation about its XML is sparse. If you want to know more about this file format, it's best to Google it, e.g., [`allintext:Moodle timeopen`](https://www.google.com/search?q=allintext:moodle+timeopen)
