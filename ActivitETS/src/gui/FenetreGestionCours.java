package gui;

import java.awt.Dimension;
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import activites.Cours;
import modele.ListeCoursTableModel;

public class FenetreGestionCours {

	private JFrame frmR;
	
	public FenetreGestionCours() {
		initialize();
	}
	
	public void initialize() {
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (ClassNotFoundException | InstantiationException
				| IllegalAccessException | UnsupportedLookAndFeelException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		// Code
		Dimension dimension = java.awt.Toolkit.getDefaultToolkit()
				.getScreenSize();
		int height = (int) dimension.getHeight() / 2;
		int width = (int) dimension.getWidth() / 2;

		frmR = new JFrame();
		frmR.setTitle("Liste des cours");
		// frmR.setResizable(false);
		frmR.setSize(width, height);
		frmR.setLocationRelativeTo(null);

		frmR.setVisible(true);
	}
	
	public void afficherListeCours(ArrayList<Cours> listeCours) {
		 
		//ListeCoursTableModel model = new ListeCoursTableModel(listeCours);
		
        //JTable tableau = new JTable(model);
        
       //frmR.add(new JScrollPane(tableau), null);
	}
}
