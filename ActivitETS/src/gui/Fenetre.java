package gui;

import javax.swing.JFrame;
import javax.swing.JFileChooser;
import javax.swing.JTabbedPane;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JTextArea;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import java.awt.GridBagLayout;

import javax.swing.JSplitPane;

import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.Color;
import java.io.File;
import java.lang.reflect.Array;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Properties;

import javax.swing.JPanel;
import javax.swing.JLabel;

import activites.Quiz;

import java.awt.Font;

import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JCheckBox;

import org.jdatepicker.impl.JDatePanelImpl;
import org.jdatepicker.impl.JDatePickerImpl;
import org.jdatepicker.impl.UtilDateModel;

import controleur.Controleur;
import utils.DateFormattedListCellRenderer;
import utils.DateLabelFormatter;
import modele.Modele;
import net.miginfocom.swing.MigLayout;

import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Fenetre extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JFrame frmR;
	private JMenuItem mntmOuvrirFichiermbz;
	private JTabbedPane tabbedPane;
	private JSplitPane splitPane;
	private JTextField txtDateOpen;
	private JTextField txtHourOpen;
	private JTextField txtDateClose;
	private JTextField txtHourClose;
	private JLabel lblCoursDbut;
	private JButton btnEnregistrer;
	JPanel panel;
	private JMenuItem mntmQuitter;
	private UtilDateModel modelOpen, modelClose;
	private Properties p;
	private JMenuItem mntmNewMenuItem;
	private JPanel panel_1;
	private JMenuItem mntmCompresserEnMbz;

	/**
	 * Create the application.
	 */
	public Fenetre() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {

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
		frmR.setTitle("ActivitETS");
		// frmR.setResizable(false);
		frmR.setSize(width, height);
		frmR.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmR.setLocationRelativeTo(null);

		JMenuBar menuBar = new JMenuBar();
		frmR.setJMenuBar(menuBar);

		JMenu mnFichier = new JMenu("Fichier");
		menuBar.add(mnFichier);

		mntmOuvrirFichiermbz = new JMenuItem("Ouvrir fichier .MBZ");
		mnFichier.add(mntmOuvrirFichiermbz);

		mntmCompresserEnMbz = new JMenuItem("Compresser en MBZ");
		mnFichier.add(mntmCompresserEnMbz);

		mntmNewMenuItem = new JMenuItem("Enregistrer");
		mnFichier.add(mntmNewMenuItem);

		mntmQuitter = new JMenuItem("Quitter");
		mnFichier.add(mntmQuitter);
		GridBagLayout gridBagLayout = new GridBagLayout();
		gridBagLayout.columnWidths = new int[] { 0, 0 };
		gridBagLayout.rowHeights = new int[] { 0, 0, 0 };
		gridBagLayout.columnWeights = new double[] { 1.0, Double.MIN_VALUE };
		gridBagLayout.rowWeights = new double[] { 1.0, 1.0, Double.MIN_VALUE };
		frmR.getContentPane().setLayout(gridBagLayout);

		splitPane = new JSplitPane();
		splitPane.setBackground(Color.WHITE);
		GridBagConstraints gbc_splitPane = new GridBagConstraints();
		gbc_splitPane.gridheight = 2;
		gbc_splitPane.insets = new Insets(0, 0, 5, 0);
		gbc_splitPane.fill = GridBagConstraints.BOTH;
		gbc_splitPane.gridx = 0;
		gbc_splitPane.gridy = 0;
		frmR.getContentPane().add(splitPane, gbc_splitPane);

		tabbedPane = new JTabbedPane(JTabbedPane.LEFT);
		tabbedPane.setBackground(Color.GRAY);
		splitPane.setLeftComponent(tabbedPane);

		panel_1 = new JPanel();
		splitPane.setRightComponent(panel_1);

		// tabbedPane.addTab("Activités", null);

		p = new Properties();
		p.put("text.today", "Today");
		p.put("text.month", "Month");
		p.put("text.year", "Year");

		/*
		 * int xSize = frmR.getWidth(); int ySize = frmR.getHeight();
		 * 
		 * int gameHeight = (int) (Math.round(ySize * 0.10)); int gameWidth =
		 * (int) (Math.round(xSize * 0.10));
		 * 
		 * btnPanel = new JPanel(new MigLayout("fill")); btnEnregistrer = new
		 * JButton("Enregistrer");
		 * 
		 * btnPanel.add(btnEnregistrer, "span, right, wrap");
		 * btnPanel.setPreferredSize(new Dimension(gameWidth, gameHeight));
		 * 
		 * GridBagConstraints gbc_panel_1 = new GridBagConstraints();
		 * gbc_panel_1.fill = GridBagConstraints.BOTH; gbc_panel_1.gridx = 0;
		 * gbc_panel_1.gridy = 1; frmR.getContentPane().add(btnPanel,
		 * gbc_panel_1);
		 */

		frmR.setVisible(true);
	}

	public String choixFic() {
		JFileChooser chooser = new JFileChooser(new File(
				"C:\\Users\\Denis\\workspace\\ActivitETS"));
		chooser.setApproveButtonText("Choix du fichier...");
		// chooser.showOpenDialog(null); // affiche la boite de dialogue
		String path = "";
		if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
			path = chooser.getSelectedFile().getAbsolutePath();

		}
		return path;
	}

	public JMenuItem getMenuFic() {
		return mntmOuvrirFichiermbz;
	}

	public JMenuItem getMenuQuitter() {
		return mntmQuitter;
	}

	public JMenuItem getMenuEnregistrer() {
		return mntmNewMenuItem;
	}

	public JMenuItem getMenuCompresser() {
		return mntmCompresserEnMbz;
	}

	public JTabbedPane getTab() {
		return tabbedPane;
	}

	public JButton getBtnCreateFic() {
		return btnEnregistrer;
	}

	public LocalDate getDateOpen() {

		LocalDate dateOpen = modelOpen.getValue().toInstant()
				.atZone(ZoneId.systemDefault()).toLocalDate();

		return dateOpen;
	}

	public LocalDate getDateClose() {

		LocalDate dateclose = modelClose.getValue().toInstant()
				.atZone(ZoneId.systemDefault()).toLocalDate();

		return dateclose;
	}

	public void afficherQuizs(ArrayList<Quiz> listeQuizs) {

		// tabbedPane.removeTabAt(0);
		for (int i = 0; i < listeQuizs.size(); ++i) {
			JPanel panelTab = new JPanel(new MigLayout("fill"));
			splitPane.setRightComponent(panelTab);
			tabbedPane.addTab(listeQuizs.get(i).getNom(), panelTab);

			JLabel lblNomQuiz = new JLabel(listeQuizs.get(i).getNom());
			lblNomQuiz.setFont(new Font("Tahoma", Font.PLAIN, 18));
			panelTab.add(lblNomQuiz, "center,span, wrap");

			JPanel resumePanel = new JPanel(new MigLayout());

			JLabel lblRsumDuQuiz = new JLabel("Résumé du Quiz :");
			resumePanel.add(lblRsumDuQuiz);

			JTextArea txtCeMinitestVise = new JTextArea();
			String resume = listeQuizs.get(i).getResume();
			txtCeMinitestVise.setText(resume);
			txtCeMinitestVise.setEditable(false);
			txtCeMinitestVise.setLineWrap(true);
			// txtCeMinitestVise.setMinimumSize(resumePanel.getMaximumSize());
			txtCeMinitestVise.setSize(500, 80);
			resumePanel.add(txtCeMinitestVise);

			panelTab.add(resumePanel, "center, span 7, wrap");

			JPanel chexkboxPanel = new JPanel(new MigLayout("fill"));

			JCheckBox chckbxNewCheckBox = new JCheckBox("Par date :");
			chexkboxPanel.add(chckbxNewCheckBox);

			JPanel datePanel = new JPanel(new MigLayout("fill"));

			UtilDateModel modelOpen = new UtilDateModel();
			modelOpen.setDate(listeQuizs.get(i).getDateOpen().getYear(),
					listeQuizs.get(i).getDateOpen().getMonthValue() - 1,
					listeQuizs.get(i).getDateOpen().getDayOfMonth());
			modelOpen.setSelected(true);
			JDatePanelImpl datePanelImplOpen = new JDatePanelImpl(modelOpen, p);
			JDatePickerImpl datePickerOpen = new JDatePickerImpl(
					datePanelImplOpen, new DateLabelFormatter());
			datePickerOpen.setTextEditable(true);

			datePanel.add(datePickerOpen, "grow");

			// txtDateOpen = new JTextField();
			// txtDateOpen.setText(listeQuizs.get(i).getDateOpen().toString().split("T")[0]);
			// datePanel.add(txtDateOpen, "grow");

			/*
			 * final JFXPanel fxPanel = new JFXPanel(); datePanel.add(fxPanel,
			 * "grow");
			 */
			// initFX(fxPanel);
			/*
			 * Platform.runLater(new Runnable() {
			 * 
			 * @Override public void run() { initFX(fxPanel); } });
			 */

			// datePanel.add(dateOpenPicker, "grow");

			JLabel lblAOpen = new JLabel("à");
			datePanel.add(lblAOpen, "grow");

			txtHourOpen = new JTextField();
			txtHourOpen.setText(listeQuizs.get(i).getDateOpen().toString()
					.split("T")[1]);

			JComboBox<LocalTime> cbHourOpen = setHeureCombobox(listeQuizs
					.get(i).getDateOpen().toString().split("T")[1]);
			cbHourOpen.setEditable(true);
			datePanel.add(cbHourOpen, "grow");

			JLabel lblAu = new JLabel("au");
			datePanel.add(lblAu, "grow");

			UtilDateModel modelClose = new UtilDateModel();
			modelClose.setDate(listeQuizs.get(i).getDateClose().getYear(),
					listeQuizs.get(i).getDateClose().getMonthValue() - 1,
					listeQuizs.get(i).getDateClose().getDayOfMonth());
			modelClose.setSelected(true);
			JDatePanelImpl datePanelImplClose = new JDatePanelImpl(modelClose,
					p);
			JDatePickerImpl datePickerClose = new JDatePickerImpl(
					datePanelImplClose, new DateLabelFormatter());
			datePickerClose.setTextEditable(true);

			datePanel.add(datePickerClose, "grow");

			JLabel lblAClose = new JLabel("à");
			datePanel.add(lblAClose, "grow");

			JComboBox<LocalTime> cbHourClose = setHeureCombobox(listeQuizs
					.get(i).getDateClose().toString().split("T")[1]);
			cbHourClose.setEditable(true);
			datePanel.add(cbHourClose, "grow");

			panelTab.add(datePanel, "span, center, wrap");

			JCheckBox chckbxParCours = new JCheckBox("Par cours :");
			chexkboxPanel.add(chckbxParCours);

			// panelTab.add(chexkboxPanel);

			JPanel coursPanel = new JPanel(new MigLayout("fill"));

			lblCoursDbut = new JLabel("Cours début :");
			coursPanel.add(lblCoursDbut);

			String[] data = { "Cours 1", "Cours 2", "Cours 3", "Cours 4",
					"Cours 5", "Cours 6", "Cours 7" };

			JComboBox comboBox = new JComboBox();
			comboBox.setModel(new DefaultComboBoxModel(new String[] {
					"Cours 1", "Cours 2", "Cours 3", "Cours 4" }));
			coursPanel.add(comboBox);

			JLabel label_1 = new JLabel("Cours fin :");
			coursPanel.add(label_1);

			JComboBox comboBox_1 = new JComboBox();
			comboBox_1.setModel(new DefaultComboBoxModel(new String[] {
					"Cours 1", "Cours 2", "Cours 3", "Cours 4" }));
			coursPanel.add(comboBox_1);

			//panelTab.add(coursPanel, "span, center, wrap");

			JPanel btnPanel = new JPanel(new MigLayout("fill"));

			btnEnregistrer = new JButton("Enregistrer");
			btnPanel.add(btnEnregistrer);

			Quiz quiz = listeQuizs.get(i);

			btnEnregistrer.addActionListener(new ActionListener() {

				@Override
				public void actionPerformed(ActionEvent e) {

					//System.out.println("heure : " + (((LocalTime) cbHourOpen.getSelectedItem()).getHour()));
					
					
					LocalDateTime dateOpen = LocalDateTime.of(datePickerOpen.getModel().getYear(), 
															  datePickerOpen.getModel().getMonth() + 1,
															  datePickerOpen.getModel().getDay(), 
															  (Integer.valueOf(cbHourOpen.getSelectedItem().toString().split(":")[0])), 
															  (Integer.valueOf(cbHourOpen.getSelectedItem().toString().split(":")[1])));
					LocalDateTime dateClose = LocalDateTime.of(datePickerClose.getModel().getYear(), 
															   datePickerClose.getModel().getMonth() + 1, 
															   datePickerClose.getModel().getDay(), 
															   (Integer.valueOf(cbHourClose.getSelectedItem().toString().split(":")[0])), 
															   (Integer.valueOf(cbHourClose.getSelectedItem().toString().split(":")[1])));

					ArrayList<LocalDateTime> listeNewDates = new ArrayList<LocalDateTime>();
					listeNewDates.add(dateOpen);
					listeNewDates.add(dateClose);
					quiz.setDateOpen(dateOpen);
					quiz.setDateClose(dateClose);
					System.out.println("heure2 : ");
					//System.out.println("Nom quiz : " + quiz.getNom()  + " // resume : " + quiz.getResume());
					String pathNewFile = quiz.getPath();
					generateNewFile(listeNewDates, pathNewFile);
				}
			});

			panelTab.add(btnPanel, "span, right, wrap");
		}

	}

	// Test date picker en JAVA FX
	/*
	 * private static void initFX(JFXPanel fxPanel) { // This method is invoked
	 * on the JavaFX thread Group root = new Group(); Scene scene = new
	 * Scene(root);
	 * 
	 * GridPane gridPane = new GridPane(); gridPane.setHgap(10);
	 * gridPane.setVgap(10);
	 * 
	 * String pattern = "yyyy-MM-dd"; StringConverter converter = new
	 * StringConverter<LocalDate>() { DateTimeFormatter dateFormatter =
	 * DateTimeFormatter.ofPattern(pattern);
	 * 
	 * @Override public String toString(LocalDate date) { if (date != null) {
	 * return dateFormatter.format(date); } else { return ""; } }
	 * 
	 * @Override public LocalDate fromString(String string) { if (string != null
	 * && !string.isEmpty()) { return LocalDate.parse(string, dateFormatter); }
	 * else { return null; } } };
	 * 
	 * Label checkInlabel = new Label("Date open:"); gridPane.add(checkInlabel,
	 * 0, 0); GridPane.setHalignment(checkInlabel, HPos.LEFT);
	 * 
	 * DatePicker dateOpenPicker = new DatePicker();
	 * dateOpenPicker.setConverter(converter);
	 * dateOpenPicker.setPromptText(pattern.toLowerCase());
	 * gridPane.add(dateOpenPicker, 1, 0);
	 * 
	 * 
	 * root.getChildren().add(gridPane);
	 * 
	 * fxPanel.setScene(scene);
	 * 
	 * }
	 */

	public void afficherTab(JTabbedPane tab) {
	}

	public ArrayList<LocalDateTime> recupererDates() {

		ArrayList<LocalDateTime> listeDates = new ArrayList<LocalDateTime>();

		LocalDateTime dateOpen = LocalDateTime.of(modelOpen.getYear(),
				modelOpen.getMonth(), modelOpen.getDay(),
				Integer.valueOf(txtHourOpen.toString().split(":")[0]),
				Integer.valueOf(txtHourOpen.toString().split(":")[1]));
		LocalDateTime dateClose = LocalDateTime.of(modelClose.getYear(),
				modelClose.getMonth(), modelClose.getDay(),
				Integer.valueOf(txtHourClose.toString().split(":")[0]),
				Integer.valueOf(txtHourClose.toString().split(":")[1]));

		listeDates.add(dateOpen);
		listeDates.add(dateClose);

		return listeDates;

	}

	private JComboBox setHeureCombobox(String heure) {

		LocalTime time = LocalTime.of(Integer.valueOf(heure.split(":")[0]),
				Integer.valueOf(heure.split(":")[1]));
		LocalTime time2 = LocalTime.of(Integer.valueOf(heure.split(":")[0]),
				Integer.valueOf(heure.split(":")[1]));
		LocalTime l = LocalTime.now();

		DefaultComboBoxModel<LocalTime> model = new DefaultComboBoxModel<>();
		do {
			model.addElement(time);
			time = time.plusMinutes(15);
		} while (!time.equals(time2));

		JComboBox<LocalTime> cb = new JComboBox<>(model);
		cb.setRenderer(new DateFormattedListCellRenderer(new SimpleDateFormat(
				"HH:mm")));

		return cb;

	}

	private void generateNewFile(ArrayList<LocalDateTime> listesNewDates,
			String pathNewFile) {

		for (int i = 0; i < listesNewDates.size(); ++i) {
			System.out.println("Date : " + listesNewDates.get(i).toString()
					+ " //timestamp : " + listesNewDates.get(i));
		}
		Modele modele = new Modele();
		modele.createNewXML(listesNewDates, pathNewFile);
	}
	
	public void afficherFicCompresseOK() {
		JOptionPane.showMessageDialog(frmR, "L'archive a bien été compressée.");
	}
}
