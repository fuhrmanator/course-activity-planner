package modele;

import java.awt.Component;
import java.text.SimpleDateFormat;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import javax.swing.DefaultCellEditor;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JSpinner;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SpinnerNumberModel;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableModel;

import activites.Cours;
import activites.Quiz;
import utils.DateFormattedListCellRenderer;

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

	public boolean isCellEditable(int row, int column) {
		return true;
	}

	@Override
	public void setValueAt(Object aValue, int rowIndex, int columnIndex) {
		/*if (columnIndex == 4) {
			calendarDebut.setTime((Date) aValue);
		} else if (columnIndex == 5) {
			calendarFin.setTime((Date) aValue);
		}
		if (columnIndex == 3) {
			quiz = (Quiz) aValue;
		}*/
		
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
		//this.calendarDebut = calendar;
		//this.calendarFin = calendarF;
		fireTableDataChanged();
	}

}
