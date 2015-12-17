package controleur;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.time.LocalDateTime;
import java.util.ArrayList;

import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JTabbedPane;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import activites.Activite;
import activites.Cours;
import activites.Quiz;
import gui.Fenetre;
import modele.Modele;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 * 
 * Controleur de l'architecture MVC
 */


public class Controleur{

	private Modele modele;
	private JFrame vue;
	private ActionListener actionListener;
	private ChangeListener changeListener;
	private ArrayList<Cours> listeCours;
	private ArrayList<Quiz> listeQuizs;

	public Controleur(Modele modele, JFrame vue) {
		this.modele = modele;
		this.vue = vue;
	}

	public void control() {

		//Ouvrir une sauvegarde Moodle et afficher les activités
		((Fenetre) vue).getMenuFic().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent e) {
				String path = ((Fenetre) vue).choixFic();
				ouvrirFic(path);
				afficherInfos();
			}
		});
		
		//Importer les cours depuis un .ics et les afficher
		((Fenetre) vue).getMenuCalendrier().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent e) {
				String pathCalendrier = ((Fenetre) vue).choixFic();
				listeCours = modele.recupererCours(pathCalendrier);
				((Fenetre) vue).afficherListeCours(listeCours, listeQuizs);
				modele.syncCoursQuizs(listeCours, listeQuizs);
				
				((Fenetre) vue).syncCoursQuizs(listeCours, listeQuizs);
			}
		});

		//Quitter l'app
		((Fenetre) vue).getMenuQuitter().addActionListener(
				new AbstractAction() {

					@Override
					public void actionPerformed(ActionEvent e) {
						System.exit(0);
					}
				});
		
		//COmpresser les activités dans une nouvelle sauvegarde .mbz compatible Moodle
		((Fenetre) vue).getMenuCompresser().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				
				modele.createNewMBZ("MoodleBackup.taz.gz");
				((Fenetre) vue).afficherFicCompresseOK();
			}
		});
		
		//Synchroniser les quizs avec les cours
		((Fenetre) vue).getBtnSyncCoursQuizs().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				
				modele.syncCoursQuizs(listeCours, listeQuizs);
				
				((Fenetre) vue).syncCoursQuizs(listeCours, listeQuizs);
			}
		});
		
		
		((Fenetre) vue).getBtnSetDeltas().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				
				
			}
		});

	}

	private void ouvrirFic(String path) {

		listeQuizs = modele.recupererActivites(path);
		for (int i = 0; i < listeQuizs.size(); ++i) {
			String pathNameFic = listeQuizs.get(i).getPath();
			modele.recupererInfosQuiz(pathNameFic, listeQuizs.get(i));
		}
		((Fenetre) vue).afficherQuizs(listeQuizs);

	}

	private void afficherInfos() {

		/*
		 * Quiz quiz = modele.recupererInfos(); ((Gui) vue).afficherInfos(quiz);
		 */
	}

	//Génère la nouvelle sauvegarde Moodle
	private void generateNewFile(ArrayList<LocalDateTime> listesNewDates,
			String pathNewFile) {

		for (int i = 0; i < listesNewDates.size(); ++i) {
			System.out.println("Date : " + listesNewDates.get(i).toString()
					+ " //timestamp : " + listesNewDates.get(i));
		}

		modele.createNewXML(listesNewDates, pathNewFile);
	}

}
