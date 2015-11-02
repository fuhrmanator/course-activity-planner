package modele;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import org.apache.commons.compress.archivers.ArchiveException;

import activites.Activite;
import activites.Quiz;
import utils.MoodleBackupFile;
import utils.MoodleImportBackup;
import utils.OperationsFichiers;

public class Modele {

	private LocalDateTime dateStart, dateStop;
	private String quizName, quizResume;
	//public Quiz quiz = new Quiz();
	OperationsFichiers operationsFics = new OperationsFichiers();
	MoodleBackupFile backup = new MoodleBackupFile();
	
	public ArrayList<Quiz> recupererActivites(String path) {
		
		//ArrayList<Activite> activites = new ArrayList<Activite>();
		ArrayList<Quiz> quizs = new ArrayList<Quiz>();
		String pathExctract = "MoodleBackup";
		String pathActivities = pathExctract + "\\activities";
		//path = "C:\\Users\\Denis\\workspace\\ActivitETS\\backup-moodle2-course-nu.mbz";
		File fToExctract = new File(path);
		File fExtract = new File(pathExctract);
		File fActivite = new File(pathActivities);
		//operationsFics.lireFic(path);
		
		try {
			backup.unzip(path, pathExctract);
			quizs = operationsFics.retournerListeActivites(fActivite);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ArchiveException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		dateStart = operationsFics.getDateOpen();
		dateStop = operationsFics.getDateClose();

		

		
		//System.out.println(quiz.getDateStart().toString());

		return quizs;
	}
	
	public void recupererInfosQuiz(String fic, Quiz quiz) {
		operationsFics.lireFic(fic, quiz);
	}
	
	/*public Quiz recupererInfos() {
		
		quizName = operationsFics.getQuizName();
		quizResume = operationsFics.getQuizResume();
		
		return quiz;
	}*/
	
	public void createNewXML(ArrayList<LocalDateTime> listesNewDates, String pathNewFile) {
		
		operationsFics.ecrireFichier(listesNewDates, pathNewFile);
	}
	
	public void createNewMBZ(String fileToZip) {
		/*File fileCompress = new File(fileToZip);
		
		File fileToCompress = new File("MoodleBackup\\\\");
		MoodleImportBackup moodleImport = new MoodleImportBackup();
		moodleImport.compress(fileToCompress, fileCompress);*/
		backup.zipIt(fileToZip);
	}
	
}
