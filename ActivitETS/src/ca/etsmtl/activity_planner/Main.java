package ca.etsmtl.activity_planner;

import ca.etsmtl.activity_planner.controleur.Controleur;
import ca.etsmtl.activity_planner.gui.Fenetre;
import ca.etsmtl.activity_planner.modele.Modele;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 *
 * Main Class
 */

public class Main {

	public static void main(String[] args) {

		/*
		 * Démarre l'appli
		 */
		Modele modele = new Modele();
		Fenetre vue = new Fenetre();
		Controleur controller = new Controleur(modele, vue);
		controller.control();
		vue.setVisible(true);

	}

}
