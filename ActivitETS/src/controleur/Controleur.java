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
import activites.Quiz;
import gui.Fenetre;
import gui.Gui;
import modele.Modele;

public class Controleur{

	private Modele modele;
	// private Fenetre vue;
	private JFrame vue;
	private ActionListener actionListener;
	private ChangeListener changeListener;

	public Controleur(Modele modele, JFrame vue) {
		this.modele = modele;
		this.vue = vue;
	}

	public void control() {
		/*
		 * actionListener = new ActionListener() {
		 * 
		 * @Override public void actionPerformed(ActionEvent actionEvent) {
		 * if(actionEvent.getSource() == ((Fenetre)vue).getMenuFic()) { String
		 * path = ((Fenetre)vue).choixFic(); ouvrirFic(path); afficherInfos(); }
		 * else if(actionEvent.getSource() == ((Gui) vue).getBtnCreateFic()) {
		 * String pathNewFile = "QuizzMoodle\\activities\\quizTest.xml";
		 * ArrayList<LocalDateTime> listesNewDates = ((Gui) vue).getNewDates();
		 * generateNewFile(listesNewDates, pathNewFile); }
		 * 
		 * }
		 * 
		 * };
		 */
		
		//start();

		((Fenetre) vue).getMenuFic().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent e) {
				String path = ((Fenetre) vue).choixFic();
				ouvrirFic(path);
				afficherInfos();
			}
		});

		((Fenetre) vue).getMenuQuitter().addActionListener(
				new AbstractAction() {

					@Override
					public void actionPerformed(ActionEvent e) {
						System.exit(0);
					}
				});
		
		((Fenetre) vue).getMenuCompresser().addActionListener(new AbstractAction() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				
				modele.createNewMBZ("MoodleBackup.taz.gz");
				((Fenetre) vue).afficherFicCompresseOK();
			}
		});

	}

	private void ouvrirFic(String path) {
		// if(path.contains("quiz.xml")) {
		// ArrayList<Activite> listeActivites = modele.recupererActivites(path);
		ArrayList<Quiz> listeQuizs = modele.recupererActivites(path);
		for (int i = 0; i < listeQuizs.size(); ++i) {
			String pathNameFic = listeQuizs.get(i).getPath();
			modele.recupererInfosQuiz(pathNameFic, listeQuizs.get(i));
		}
		((Fenetre) vue).afficherQuizs(listeQuizs);

		/*
		 * } else { ((Gui) vue).afficherEreurFichier(); }
		 */

	}

	private void afficherInfos() {

		/*
		 * Quiz quiz = modele.recupererInfos(); ((Gui) vue).afficherInfos(quiz);
		 */
	}

	private void generateNewFile(ArrayList<LocalDateTime> listesNewDates,
			String pathNewFile) {

		for (int i = 0; i < listesNewDates.size(); ++i) {
			System.out.println("Date : " + listesNewDates.get(i).toString()
					+ " //timestamp : " + listesNewDates.get(i));
		}

		modele.createNewXML(listesNewDates, pathNewFile);
	}

}
