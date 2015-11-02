package gui;

import javax.swing.*;

import org.jdatepicker.impl.JDatePanelImpl;
import org.jdatepicker.impl.JDatePickerImpl;
import org.jdatepicker.impl.UtilDateModel;

import activites.Quiz;
import utils.DateLabelFormatter;
import utils.OperationsFichiers;
import utils.SpinnerTemporalEditor;
import utils.SpinnerTemporalModel;

import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.*;
import java.io.File;
import java.io.FileReader;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.time.temporal.TemporalField;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Properties;

public class Gui extends JFrame {

	JButton btnFileChooser, btnGenerateNewFic; 
	JTextField status = new JTextField("Pas de fichier chargé!");
	JLabel lblTitleName, lblTitleResume, lblTitleDateStart, lblTitleDateStop, lblDateStart, lblDateStop, quizName, quizResume;
	GridLayout gridLayout = new GridLayout(7,2);
	UtilDateModel modelOpen, modelClose;
	JDatePickerImpl datePickerOpen, datePickerClose;
	JSpinner timeSpinnerOpen, timeSpinnerClose;
	ArrayList<LocalDateTime> newDates;
	LocalDateTime dateOpen, dateClose;
	SpinnerTemporalModel spinnerTempOpen, spinnerTempClose;
	
	
	public Gui() {

		
		super("ActivitETS");

		btnFileChooser = new JButton("Importer fichier XML");
		btnGenerateNewFic = new JButton("Exporter le nouveau fichier XML");
		lblDateStart = new JLabel();
		lblDateStop = new JLabel();
		lblTitleName = new JLabel("Nom du quiz :");
		lblTitleResume = new JLabel("Résumé du quiz :");
		lblTitleDateStart = new JLabel("Date de debut :");
		lblTitleDateStop = new JLabel("Date de fin :");
		
		Properties p = new Properties();
		p.put("text.today", "Today");
		p.put("text.month", "Month");
		p.put("text.year", "Year");

		//Modele pour la date d'ouverture
		modelOpen = new UtilDateModel();
		JDatePanelImpl datePanelOpen = new JDatePanelImpl(modelOpen, p);
		datePickerOpen = new JDatePickerImpl(datePanelOpen, new DateLabelFormatter());
		
		//Modele pour la date de fermeture
		modelClose = new UtilDateModel();
		JDatePanelImpl datePanelClose = new JDatePanelImpl(modelClose, p);
		datePickerClose = new JDatePickerImpl(datePanelClose, new DateLabelFormatter());	

		//Modele pour l'heure d'ouveture
		spinnerTempOpen = new SpinnerTemporalModel(LocalTime.now(), LocalTime.of(0, 0, 0), LocalTime.of(23, 59, 59), ChronoUnit.SECONDS);
		timeSpinnerOpen = new JSpinner(spinnerTempOpen);
		timeSpinnerOpen.setEditor(new SpinnerTemporalEditor(timeSpinnerOpen, DateTimeFormatter.ofPattern("HH:mm:ss")));
			
		//Modele pour l'heure de fermeture
		spinnerTempClose = new SpinnerTemporalModel(LocalTime.now(), LocalTime.of(0, 0, 0), LocalTime.of(23, 59, 59), ChronoUnit.SECONDS);
		timeSpinnerClose = new JSpinner(spinnerTempClose);
		timeSpinnerClose.setEditor(new SpinnerTemporalEditor(timeSpinnerClose, DateTimeFormatter.ofPattern("HH:mm:ss")));
		
		quizName = new JLabel();
		quizResume = new JLabel();
		
		this.setTitle("ActivitETS");
		this.setSize(700, 250);
		this.setLocationRelativeTo(null);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setVisible(true);


		JPanel panneau = new JPanel();
		panneau.setLayout(gridLayout);
		panneau.add(btnFileChooser);
		panneau.add(status);
		panneau.add(lblTitleName);
		panneau.add(lblTitleResume);
		panneau.add(quizName);
		panneau.add(quizResume);
		panneau.add(lblTitleDateStart);
		panneau.add(lblTitleDateStop);
		panneau.add(datePickerOpen);
		panneau.add(datePickerClose);
		panneau.add(timeSpinnerOpen);
		panneau.add(timeSpinnerClose);
		panneau.add(btnGenerateNewFic);
		
		this.setContentPane(panneau);

	}

	public String choixFic() {
		JFileChooser chooser = new JFileChooser(new File("C:\\Users\\Denis\\workspace\\ActivitETS"));
		chooser.setApproveButtonText("Choix du fichier...");
		//chooser.showOpenDialog(null); // affiche la boite de dialogue
		String path = "";
		if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
			path = chooser.getSelectedFile().getAbsolutePath();

		}
		status.setText(path);
		return path;
	}

	public JButton getBtnFic() {
		return btnFileChooser;
	}
	
	public JButton getBtnCreateFic() {
		return btnGenerateNewFic;
	}
	
	public ArrayList<LocalDateTime> getNewDates() {
		
		newDates = new ArrayList<LocalDateTime>();

		
		int yearOpen = modelOpen.getYear();
		int monthOpen = modelOpen.getMonth();
		int dayOpen = modelOpen.getDay();
		int hourOpen = Integer.valueOf(spinnerTempOpen.getTemporalValue().toString().split(":")[0]);
		int minuteOpen = Integer.valueOf(spinnerTempOpen.getTemporalValue().toString().split(":")[1]);
		int secondOpen = 0;
		if(spinnerTempOpen.getTemporalValue().toString().split(":").length > 2 ) {
			secondOpen = Integer.valueOf(spinnerTempOpen.getTemporalValue().toString().split(":")[2]);
		}
		
		int yearClose = modelClose.getYear();
		int monthClose = modelClose.getMonth();
		int dayClose = modelClose.getDay();
		int hourClose = Integer.valueOf(spinnerTempClose.getTemporalValue().toString().split(":")[0]);
		int minuteClose = Integer.valueOf(spinnerTempClose.getTemporalValue().toString().split(":")[1]);
		int secondClose = 0;
		if(spinnerTempClose.getTemporalValue().toString().split(":").length > 2 ) {
			secondClose = Integer.valueOf(spinnerTempClose.getTemporalValue().toString().split(":")[2]);
		}
		
			
		dateOpen = LocalDateTime.of(yearOpen, monthOpen, dayOpen, hourOpen, minuteOpen, secondOpen);
		dateClose = LocalDateTime.of(yearClose, monthClose, dayClose, hourClose, minuteClose, secondClose);
		
		System.out.println("Date et heure open: " + dateOpen);
		System.out.println("Date et heure close: " + dateClose);
		
		newDates.add(dateOpen);
		newDates.add(dateClose);
		return newDates;
	}
	

	public void afficherDates(ArrayList<LocalDateTime> dates) {

		
		int yearOpen = dates.get(0).getYear();
		int monthOpen = dates.get(0).getMonthValue();
		int dayOpen = dates.get(0).getDayOfMonth();
		int hourOpen = dates.get(0).getHour();
		int minuteOpen = dates.get(0).getMinute();
		int secondOpen = dates.get(0).getSecond();
		
		int yearClose = dates.get(1).getYear();
		int monthClose = dates.get(1).getMonthValue();
		int dayClose = dates.get(1).getDayOfMonth();
		int hourClose = dates.get(1).getHour();
		int minuteClose = dates.get(1).getMinute();
		int secondClose = dates.get(1).getSecond();
		
		modelOpen.setDate(yearOpen, monthOpen, dayOpen);
		modelClose.setDate(yearClose, monthClose, dayClose);
		modelOpen.setSelected(true);
		modelClose.setSelected(true);
		
		timeSpinnerOpen.setValue(LocalTime.of(hourOpen, minuteOpen, secondOpen));
		timeSpinnerClose.setValue(LocalTime.of(hourClose, minuteClose, secondClose));
		
		lblDateStart.setText(dates.get(0).toString());
		lblDateStop.setText(dates.get(1).toString());

	}
	
	public void afficherInfos(Quiz quiz) {
		quizName.setText(quiz.getNom());
		quizResume.setText(quiz.getResume());
	}
	
	public void afficherEreurFichier() {
		JOptionPane.showMessageDialog(this, "Mauvais fichier");
	}
	

}