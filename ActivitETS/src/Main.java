import gui.Fenetre;
import javax.swing.JFrame;
import modele.Modele;
import controleur.Controleur;

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

	}

}
