package ca.etsmtl.activity_planner.modele;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import javax.swing.table.AbstractTableModel;

import ca.etsmtl.activity_planner.activites.Cours;
import ca.etsmtl.activity_planner.activites.Quiz;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 *
 * Model de la table contenant la liste des cours dans la fenêtre principale
 */


public class ListeCoursTableModel extends AbstractTableModel {

	private ArrayList<Cours> listeCours;
	private ArrayList<Quiz> listeQuizs;
	private Calendar calendarDebut;
	private Calendar calendarFin;
	private Quiz quiz = null;

	public ListeCoursTableModel(ArrayList<Cours> listeCours) {
		this.listeCours = new ArrayList<Cours>(listeCours);
		this.listeQuizs = new ArrayList<Quiz>();
		calendarDebut = null;
		// Calendar.getInstance()
		calendarFin = null;
	}

	@Override
	public int getRowCount() {
		return listeCours.size();
	}

	@Override
	public int getColumnCount() {
		return 4;
	}

	@Override
	public String getColumnName(int column) {
		String name = "??";
		switch (column) {
		case 0:
			name = "Séance";
			break;
		case 1:
			name = "Date Start";
			break;
		case 2:
			name = "Date Stop";
			break;
		case 3:
			name = "Quiz";
			break;
		case 4:
			name = "Delat début";
			break;
		case 5:
			name = "Delat Fin";
			break;
		}
		return name;
	}

	@Override
	public Class<?> getColumnClass(int columnIndex) {
		Class type = String.class;
		return type;
	}

	@Override
	public Object getValueAt(int rowIndex, int columnIndex) {
		Cours cours = listeCours.get(rowIndex);
		if (listeQuizs.size() > rowIndex) {
			quiz = listeQuizs.get(rowIndex);
		} else {
			quiz = null;
		}

		Object value = null;
		switch (columnIndex) {
		case 0:
			value = cours.getSommaire();
			break;
		case 1:
			value = cours.getDateStart();
			break;
		case 2:
			value = cours.getDateStop();
			break;
		case 3:
			if (quiz != null) {
				value = quiz.getNom();
			} else {
				value = "";
			}

			break;
		case 4:
			if(calendarDebut != null) {
				value = calendarDebut.getTime();
			} else {
				value = Calendar.getInstance().getTime();
			}

			break;
		case 5:
			if(calendarFin != null) {
				value = calendarFin.getTime();
			} else {

				value = Calendar.getInstance().getTime();
			}

			break;
		}
		return value;
	}

	@Override
	public boolean isCellEditable(int row, int column) {
		return true;
	}

	@Override
	public void setValueAt(Object aValue, int rowIndex, int columnIndex) {

		switch(columnIndex) {
		case 0:
			break;
		case 1:
			break;
		case 2:
			break;
		case 3:
			quiz = (Quiz) aValue;
			break;
		case 4:
			calendarDebut.setTime((Date) aValue);
			break;
		case 5:
			calendarFin.setTime((Date) aValue);
			break;
		}

		fireTableDataChanged();
	}

	public void refreshQuizs(ArrayList<Quiz> listeQuizs) {
		this.listeQuizs = new ArrayList<Quiz>(listeQuizs);
		fireTableDataChanged();
	}

	public void refreshDeltas(Object calendar) {

		System.out.println();
		fireTableDataChanged();
	}

}
