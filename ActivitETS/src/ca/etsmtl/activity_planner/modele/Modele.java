package ca.etsmtl.activity_planner.modele;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;

import org.apache.commons.compress.archivers.ArchiveException;

import ca.etsmtl.activity_planner.activites.Cours;
import ca.etsmtl.activity_planner.activites.Quiz;
import ca.etsmtl.activity_planner.utils.ImportCours;
import ca.etsmtl.activity_planner.utils.MoodleBackupFile;
import ca.etsmtl.activity_planner.utils.OperationsFichiers;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 *
 * Modele de l'architecture MVC
 */


public class Modele {

	private LocalDateTime dateStart, dateStop;
	private String quizName, quizResume;
	//public Quiz quiz = new Quiz();
	OperationsFichiers operationsFics = new OperationsFichiers();
	MoodleBackupFile backup = new MoodleBackupFile();
	ImportCours importCours = new ImportCours();

	public ArrayList<Quiz> recupererActivites(String path) {

		ArrayList<Quiz> quizs = new ArrayList<Quiz>();
		String pathExctract = "MoodleBackup";
		String pathActivities = pathExctract + "\\activities";
		File fToExctract = new File(path);
		File fExtract = new File(pathExctract);
		File fActivite = new File(pathActivities);

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

		return quizs;
	}

	public void recupererInfosQuiz(String fic, Quiz quiz) {
		operationsFics.lireFic(fic, quiz);
	}


	public void createNewXML(ArrayList<LocalDateTime> listesNewDates, String pathNewFile) {

		operationsFics.ecrireFichier(listesNewDates, pathNewFile);
	}

	public void createNewMBZ(String fileToZip) {
		backup.zipIt(fileToZip);
	}

	public ArrayList<Cours> recupererCours(String pathCalendrier) {
		ArrayList<Cours> listeCours = importCours.parseCalendar(pathCalendrier);

		Collections.sort(listeCours, Cours.CoursComparator);

		return listeCours;
	}

	public void syncCoursQuizs(ArrayList<Cours> listeCours, ArrayList<Quiz> listeQuizs) {

		int nbQuizs = listeQuizs.size();
		int nbCours = listeCours.size();

		for(int i = 0; i < nbQuizs; ++i) {
			listeQuizs.get(i).setCoursDebut(listeCours.get(i));
			listeQuizs.get(i).setDateOpen(listeCours.get(i).getDateStop());
			listeQuizs.get(i).setCoursFin(listeCours.get(i+1));
			listeQuizs.get(i).setDateClose(listeCours.get(i+1).getDateStart());

			ArrayList<LocalDateTime> listeNewDates = new ArrayList<LocalDateTime>();
			listeNewDates.add(listeQuizs.get(i).getDateOpen());
			listeNewDates.add(listeQuizs.get(i).getDateClose());
			String pathNewFile = listeQuizs.get(i).getPath();
			createNewXML(listeNewDates, pathNewFile);
		}
	}

}
