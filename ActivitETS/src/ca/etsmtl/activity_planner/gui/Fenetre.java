package ca.etsmtl.activity_planner.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Properties;

import javax.swing.DefaultComboBoxModel;
import javax.swing.DropMode;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SpinnerDateModel;
import javax.swing.TransferHandler;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.table.DefaultTableCellRenderer;

import org.jdatepicker.impl.JDatePanelImpl;
import org.jdatepicker.impl.JDatePickerImpl;
import org.jdatepicker.impl.UtilDateModel;

import ca.etsmtl.activity_planner.activites.Cours;
import ca.etsmtl.activity_planner.activites.Quiz;
import ca.etsmtl.activity_planner.modele.ListeCoursTableModel;
import ca.etsmtl.activity_planner.modele.Modele;
import ca.etsmtl.activity_planner.utils.DateFormattedListCellRenderer;
import ca.etsmtl.activity_planner.utils.DateLabelFormatter;
import ca.etsmtl.activity_planner.utils.TableRenderer;
import net.miginfocom.swing.MigLayout;

/*
 * projet : ActivitETS
 * @author : Denis BRESSAND
 * Date : 17/12/2015
 *
 * Vue principale
 */

public class Fenetre extends JFrame {

	private static final long serialVersionUID = 1L;
	private JFrame frmR;
	private JMenuItem mntmOuvrirFichiermbz;
	private JTabbedPane tabbedPane;
	private JSplitPane splitPane;
	private JTextField txtDateOpen, txtHourOpen, txtDateClose, txtHourClose, txtDateOpenReadOnly, txtHourOpenReadOnly;
	private JTextField txtDateCloseReadOnly, txtHourCloseReadOnly;
	private JLabel lblCoursDbut, lblDeltaDebut, lblDeltaFin;
	private JButton btnEnregistrer, btnSyncCoursQuizs, btnSetDeltas;
	private JPanel panel, panelImportQuiz;
	private JMenuItem mntmQuitter;
	private UtilDateModel modelOpen, modelClose;
	private Properties p;
	private JPanel panelPrincipal;
	private JMenuItem mntmCompresserEnMbz;
	private JMenuItem mntmImporterDesCours;
	private Dimension dimension;
	private int height, width;
	private JPanel panelListeCours;
	private ArrayList<Quiz> listeQuizs = new ArrayList<>();
	private JTable tableCours;
	private ListeCoursTableModel tableModel;
	private JComboBox cbBoxCours;
	private JComboBox<LocalTime> cbHourCloseReadOnly, cbHourOpenReadOnly;
	private JSpinner spinOpen, spinClose;
	private SpinnerDateModel model;

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
		} catch (ClassNotFoundException | InstantiationException | IllegalAccessException
				| UnsupportedLookAndFeelException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		// Code
		dimension = java.awt.Toolkit.getDefaultToolkit().getScreenSize();
		height = (int) dimension.getHeight() / 2;
		width = (int) dimension.getWidth() / 2;

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

		mntmCompresserEnMbz = new JMenuItem("Enregistrer");
		mnFichier.add(mntmCompresserEnMbz);

		mntmImporterDesCours = new JMenuItem("Importer des cours");
		mnFichier.add(mntmImporterDesCours);

		mntmQuitter = new JMenuItem("Quitter");
		mnFichier.add(mntmQuitter);
		GridBagLayout gridBagLayout = new GridBagLayout();
		gridBagLayout.columnWidths = new int[] { 0, 0 };
		gridBagLayout.rowHeights = new int[] { 0, 0, 0, 0 };
		gridBagLayout.columnWeights = new double[] { 1.0, Double.MIN_VALUE };
		gridBagLayout.rowWeights = new double[] { 1.0, 1.0, 1.0, Double.MIN_VALUE };
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

		panelPrincipal = new JPanel();
		splitPane.setRightComponent(panelPrincipal);

		panelListeCours = new JPanel();
		panelListeCours.setLayout(new BorderLayout());
		GridBagConstraints gbc_panel_2 = new GridBagConstraints();
		gbc_panel_2.fill = GridBagConstraints.BOTH;
		gbc_panel_2.gridx = 0;
		gbc_panel_2.gridy = 2;
		frmR.getContentPane().add(panelListeCours, gbc_panel_2);

		// tabbedPane.addTab("Activités", null);

		p = new Properties();
		p.put("text.today", "Today");
		p.put("text.month", "Month");
		p.put("text.year", "Year");

		btnSyncCoursQuizs = new JButton("Importer tous les quizs à partir de la séance n. : ");
		btnSetDeltas = new JButton("Enregistrer les deltas");
		btnSetDeltas.setVisible(false);

		frmR.setVisible(true);
	}

	public String choixFic() {
		JFileChooser chooser = new JFileChooser(new File("C:\\Users\\Denis\\workspace\\ActivitETS"));
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

	public JMenuItem getMenuCalendrier() {
		return mntmImporterDesCours;
	}

	public JMenuItem getMenuQuitter() {
		return mntmQuitter;
	}

	public JMenuItem getMenuCompresser() {
		return mntmCompresserEnMbz;
	}

	public JTabbedPane getTab() {
		return tabbedPane;
	}

	public JButton getBtnSyncCoursQuizs() {
		return btnSyncCoursQuizs;
	}

	public JButton getBtnSetDeltas() {
		return btnSetDeltas;
	}

	public LocalDate getDateOpen() {

		LocalDate dateOpen = modelOpen.getValue().toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

		return dateOpen;
	}

	public LocalDate getDateClose() {

		LocalDate dateclose = modelClose.getValue().toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

		return dateclose;
	}

	public void afficherQuizs(ArrayList<Quiz> listeQuizs) {

		listeQuizs = listeQuizs;
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
			txtCeMinitestVise.setSize(500, 80);
			resumePanel.add(txtCeMinitestVise);

			panelTab.add(resumePanel, "center, span 7, wrap");

			JPanel chexkboxPanel = new JPanel(new MigLayout("fill"));

			JCheckBox chckbxNewCheckBox = new JCheckBox("Par date :");
			chexkboxPanel.add(chckbxNewCheckBox);

			/*
			 * Panel pour la date ReadOnly
			 */
			JPanel datePanelReadOnly = new JPanel(new MigLayout("fill"));

			UtilDateModel modelOpenReadOnly = new UtilDateModel();
			modelOpenReadOnly.setDate(listeQuizs.get(i).getDateOpen().getYear(),
					listeQuizs.get(i).getDateOpen().getMonthValue() - 1,
					listeQuizs.get(i).getDateOpen().getDayOfMonth());
			modelOpenReadOnly.setSelected(true);
			JDatePanelImpl datePanelImplOpenReadOnly = new JDatePanelImpl(modelOpenReadOnly, p);
			JDatePickerImpl datePickerOpenReadOnly = new JDatePickerImpl(datePanelImplOpenReadOnly,
					new DateLabelFormatter());
			datePickerOpenReadOnly.setTextEditable(false);
			datePickerOpenReadOnly.setEnabled(false);
			datePanelReadOnly.add(datePickerOpenReadOnly, "grow");

			JLabel lblAOpen = new JLabel("à");
			datePanelReadOnly.add(lblAOpen, "grow");

			txtHourOpenReadOnly = new JTextField();
			txtHourOpenReadOnly.setText(listeQuizs.get(i).getDateOpen().toString().split("T")[1]);

			cbHourOpenReadOnly = setHeureCombobox(listeQuizs.get(i).getDateOpen().toString().split("T")[1]);
			cbHourOpenReadOnly.setEditable(true);
			cbHourOpenReadOnly.setEnabled(false);
			datePanelReadOnly.add(cbHourOpenReadOnly, "grow");

			JLabel lblAu = new JLabel("au");
			datePanelReadOnly.add(lblAu, "grow");

			UtilDateModel modelCloseReadOnly = new UtilDateModel();
			modelCloseReadOnly.setDate(listeQuizs.get(i).getDateClose().getYear(),
					listeQuizs.get(i).getDateClose().getMonthValue() - 1,
					listeQuizs.get(i).getDateClose().getDayOfMonth());
			modelCloseReadOnly.setSelected(true);
			JDatePanelImpl datePanelImplCloseReadOnly = new JDatePanelImpl(modelCloseReadOnly, p);
			JDatePickerImpl datePickerCloseReadOnly = new JDatePickerImpl(datePanelImplCloseReadOnly,
					new DateLabelFormatter());
			datePickerCloseReadOnly.setTextEditable(false);

			datePanelReadOnly.add(datePickerCloseReadOnly, "grow");

			JLabel lblAClose = new JLabel("à");
			datePanelReadOnly.add(lblAClose, "grow");

			cbHourCloseReadOnly = setHeureCombobox(listeQuizs.get(i).getDateClose().toString().split("T")[1]);
			cbHourCloseReadOnly.setEditable(true);
			cbHourCloseReadOnly.setEnabled(false);
			datePanelReadOnly.add(cbHourCloseReadOnly, "grow");

			panelTab.add(datePanelReadOnly, "span, center, wrap");

			/*
			 * Fin Panel pour la date ReadOnly
			 */

			/*
			 * Panel pour la date à changer
			 */

			JPanel datePanel = new JPanel(new MigLayout("fill"));

			UtilDateModel modelOpen = new UtilDateModel();
			modelOpen.setDate(listeQuizs.get(i).getDateOpen().getYear(),
					listeQuizs.get(i).getDateOpen().getMonthValue() - 1,
					listeQuizs.get(i).getDateOpen().getDayOfMonth());
			modelOpen.setSelected(true);
			JDatePanelImpl datePanelImplOpen = new JDatePanelImpl(modelOpen, p);
			JDatePickerImpl datePickerOpen = new JDatePickerImpl(datePanelImplOpen, new DateLabelFormatter());
			datePickerOpen.setTextEditable(true);

			datePanel.add(datePickerOpen, "grow");

			datePanel.add(lblAOpen, "grow");

			txtHourOpen = new JTextField();
			txtHourOpen.setText(listeQuizs.get(i).getDateOpen().toString().split("T")[1]);

			JComboBox<LocalTime> cbHourOpen = setHeureCombobox(
					listeQuizs.get(i).getDateOpen().toString().split("T")[1]);
			cbHourOpen.setEditable(true);
			datePanel.add(cbHourOpen, "grow");

			datePanel.add(lblAu, "grow");

			UtilDateModel modelClose = new UtilDateModel();
			modelClose.setDate(listeQuizs.get(i).getDateClose().getYear(),
					listeQuizs.get(i).getDateClose().getMonthValue() - 1,
					listeQuizs.get(i).getDateClose().getDayOfMonth());
			modelClose.setSelected(true);
			JDatePanelImpl datePanelImplClose = new JDatePanelImpl(modelClose, p);
			JDatePickerImpl datePickerClose = new JDatePickerImpl(datePanelImplClose, new DateLabelFormatter());
			datePickerClose.setTextEditable(true);

			datePanel.add(datePickerClose, "grow");

			datePanel.add(lblAClose, "grow");

			JComboBox<LocalTime> cbHourClose = setHeureCombobox(
					listeQuizs.get(i).getDateClose().toString().split("T")[1]);
			cbHourClose.setEditable(true);
			datePanel.add(cbHourClose, "grow");

			panelTab.add(datePanel, "span, center, wrap");

			/*
			 * Fin Panel pour la date à changer
			 */

			JCheckBox chckbxParCours = new JCheckBox("Par cours :");
			chexkboxPanel.add(chckbxParCours);

			JPanel btnPanel = new JPanel(new MigLayout("fill"));

			btnEnregistrer = new JButton("Enregistrer");
			btnPanel.add(btnEnregistrer);

			Quiz quiz = listeQuizs.get(i);

			btnEnregistrer.addActionListener(new ActionListener() {

				@Override
				public void actionPerformed(ActionEvent e) {

					LocalDateTime dateOpen = LocalDateTime.of(datePickerOpen.getModel().getYear(),
							datePickerOpen.getModel().getMonth() + 1, datePickerOpen.getModel().getDay(),
							(Integer.valueOf(cbHourOpen.getSelectedItem().toString().split(":")[0])),
							(Integer.valueOf(cbHourOpen.getSelectedItem().toString().split(":")[1])));
					LocalDateTime dateClose = LocalDateTime.of(datePickerClose.getModel().getYear(),
							datePickerClose.getModel().getMonth() + 1, datePickerClose.getModel().getDay(),
							(Integer.valueOf(cbHourClose.getSelectedItem().toString().split(":")[0])),
							(Integer.valueOf(cbHourClose.getSelectedItem().toString().split(":")[1])));

					ArrayList<LocalDateTime> listeNewDates = new ArrayList<LocalDateTime>();
					listeNewDates.add(dateOpen);
					listeNewDates.add(dateClose);
					quiz.setDateOpen(dateOpen);
					quiz.setDateClose(dateClose);
					System.out.println("heure2 : ");
					// System.out.println("Nom quiz : " + quiz.getNom() + " //
					// resume : " + quiz.getResume());
					String pathNewFile = quiz.getPath();
					generateNewFile(listeNewDates, pathNewFile);
				}
			});

			panelTab.add(btnPanel, "span, right, wrap");
		}

	}

	private JComboBox setHeureCombobox(String heure) {

		LocalTime time = LocalTime.of(Integer.valueOf(heure.split(":")[0]), Integer.valueOf(heure.split(":")[1]));
		LocalTime time2 = LocalTime.of(Integer.valueOf(heure.split(":")[0]), Integer.valueOf(heure.split(":")[1]));
		LocalTime l = LocalTime.now();

		DefaultComboBoxModel<LocalTime> model = new DefaultComboBoxModel<>();
		do {
			model.addElement(time);
			time = time.plusMinutes(15);
		} while (!time.equals(time2));

		JComboBox<LocalTime> cb = new JComboBox<>(model);
		cb.setRenderer(new DateFormattedListCellRenderer(new SimpleDateFormat("HH:mm")));

		return cb;

	}

	/*
	 * Enregistre les changements et creer un nouveau fichier compréssé
	 */
	private void generateNewFile(ArrayList<LocalDateTime> listesNewDates, String pathNewFile) {

		for (int i = 0; i < listesNewDates.size(); ++i) {
			System.out
					.println("Date : " + listesNewDates.get(i).toString() + " //timestamp : " + listesNewDates.get(i));
		}
		Modele modele = new Modele();
		modele.createNewXML(listesNewDates, pathNewFile);
	}

	public void afficherFicCompresseOK() {
		JOptionPane.showMessageDialog(frmR, "L'archive a bien été compressée.");
	}

	/*
	 * Affiche la liste des cours importés
	 */
	public void afficherListeCours(ArrayList<Cours> listeCours, ArrayList<Quiz> listeQuizs) {

		frmR.setExtendedState(frmR.MAXIMIZED_BOTH);

		tableModel = new ListeCoursTableModel(listeCours);
		cbBoxCours = new JComboBox(listeCours.toArray());

		spinOpen = new JSpinner(setJspinnerEditor(model));
		JSpinner.DateEditor de = new JSpinner.DateEditor(spinOpen, "hh:mm");
		de.getTextField().setEditable(true);
		spinOpen.setEditor(de);
		spinOpen.setVisible(false);

		spinClose = new JSpinner(setJspinnerEditor(model));
		JSpinner.DateEditor deClose = new JSpinner.DateEditor(spinClose, "hh:mm");
		deClose.getTextField().setEditable(true);
		spinClose.setEditor(deClose);
		spinClose.setVisible(false);

		/*
		 * Override pour DnD des cellules de la table
		 */
		tableCours = new JTable(tableModel);

		DefaultTableCellRenderer renderer = new TableRenderer();
		Calendar calendar = Calendar.getInstance();
		SpinnerDateModel spinnerModel = new SpinnerDateModel(calendar.getTime(), null, null, Calendar.HOUR_OF_DAY);
		// tableCours.getColumnModel().getColumn(4).setCellEditor(new
		// SpinnerEditor(spinnerModel, tableModel));
		// tableCours.getColumnModel().getColumn(5).setCellEditor(new
		// SpinnerEditor(spinnerModel, tableModel));
		tableCours.setDefaultRenderer(Object.class, renderer);
		/*
		 * tableCours.setDragEnabled(true);
		 * tableCours.setDropMode(DropMode.USE_SELECTION);
		 * tableCours.setTransferHandler(new TransferHelper());
		 */
		renderer.setHorizontalAlignment(JLabel.CENTER);

		tableCours.setDragEnabled(true);
		tableCours.setDropMode(DropMode.USE_SELECTION);
		tableCours.setTransferHandler(new TransferHelper());
		tableCours.setRowSelectionAllowed(false);
		tableCours.setCellSelectionEnabled(true);

		/*
		 * Drag&Drop cellules des tables
		 */

		/*tableCours.setTransferHandler(new TransferHandler() {

			public int getSourceActions(JComponent c) {
				return DnDConstants.ACTION_COPY_OR_MOVE;
			}

			public Transferable createTransferable(JComponent comp) {
				JTable table = (JTable) comp;
				int row = table.getSelectedRow();
				int col = table.getSelectedColumn();

				String value = (String) table.getModel().getValueAt(row, col);
				StringSelection transferable = new StringSelection(value);
				table.getModel().setValueAt(null, row, col);
				return transferable;
			}

			public boolean canImport(TransferHandler.TransferSupport info) {
				if (!info.isDataFlavorSupported(DataFlavor.stringFlavor)) {
					return false;
				}

				return true;
			}

			public boolean importData(TransferSupport support) {

				if (!support.isDrop()) {
					return false;
				}

				if (!canImport(support)) {
					return false;
				}

				JTable table = (JTable) support.getComponent();
				DefaultTableModel tableModel = (DefaultTableModel) table.getModel();

				JTable.DropLocation dl = (JTable.DropLocation) support.getDropLocation();

				int row = dl.getRow();
				int col = dl.getColumn();

				String data;
				try {
					data = (String) support.getTransferable().getTransferData(DataFlavor.stringFlavor);
				} catch (UnsupportedFlavorException e) {
					return false;
				} catch (IOException e) {
					return false;
				}

				tableModel.setValueAt(data, row, col);

				return true;
			}
		});*/

		/*
		 * TableColumn deltaDebutColumn =
		 * tableCours.getColumnModel().getColumn(4);
		 * deltaDebutColumn.setCellEditor(new DefaultCellEditor(cbBoxCours));
		 */

		panelListeCours.add("North", new JScrollPane(tableCours));
		// panelListeCours.setLayout(new MigLayout("fill"));
		panelImportQuiz = new JPanel();
		panelImportQuiz.setLayout(new MigLayout("fill"));

		lblDeltaDebut = new JLabel("delta début : + ");
		lblDeltaDebut.setVisible(false);
		lblDeltaFin = new JLabel("delta fin : - ");
		lblDeltaFin.setVisible(false);

		// panelImportQuiz.add(btnSyncCoursQuizs);
		// panelImportQuiz.add(cbBoxCours, "wrap");
		panelImportQuiz.add(lblDeltaDebut);
		panelImportQuiz.add(spinOpen);
		panelImportQuiz.add(lblDeltaFin);
		panelImportQuiz.add(spinClose);
		panelImportQuiz.add(btnSetDeltas, "wrap");

		panelListeCours.add("Center", panelImportQuiz);
	}

	@SuppressWarnings("unchecked")
	public void syncCoursQuizs(ArrayList<Cours> listeCours, ArrayList<Quiz> listeQuizs) {

		int rows = tableCours.getModel().getRowCount();
		/*
		 * for(int i = 0; i < listeQuizs.size(); ++i) {
		 * tableCours.getModel().setValueAt(listeQuizs.get(i), i, 3); }
		 */
		tableModel.refreshQuizs(listeQuizs);
		for (int i = 0; i < listeQuizs.size(); ++i) {
			cbHourOpenReadOnly = setHeureCombobox(listeQuizs.get(i).getDateOpen().toString().split("T")[1]);

			cbHourCloseReadOnly = setHeureCombobox(listeQuizs.get(i).getDateClose().toString().split("T")[1]);
			System.out.println(listeQuizs.get(i).getNom() + " // Date Open : " + listeQuizs.get(i).getDateOpen()
					+ " // Date Close : " + listeQuizs.get(i).getDateClose());
		}

		spinOpen.setVisible(true);
		spinClose.setVisible(true);
		btnSetDeltas.setVisible(true);
		lblDeltaDebut.setVisible(true);
		lblDeltaFin.setVisible(true);
		revalidate();
		repaint();

	}

	private SpinnerDateModel setJspinnerEditor(SpinnerDateModel model) {

		Date initDate = new Date();
		model = new SpinnerDateModel(initDate, null, null, Calendar.HOUR);

		return model;
	}

	public static final DataFlavor CELL_DATA_FLAVOR = createConstant(CellData.class, "application/x-java-celldata");

	static protected DataFlavor createConstant(Class clazz, String name) {
		try {
			return new DataFlavor(clazz, name);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}

	public class CellDataTransferable implements Transferable {


		private CellData cellData;

		public CellDataTransferable(CellData cellData) {
			this.cellData = cellData;
		}

		@Override
		public DataFlavor[] getTransferDataFlavors() {
			return new DataFlavor[] { CELL_DATA_FLAVOR };
		}

		@Override
		public boolean isDataFlavorSupported(DataFlavor flavor) {
			boolean supported = false;
			for (DataFlavor available : getTransferDataFlavors()) {
				if (available.equals(flavor)) {
					supported = true;
				}
			}
			return supported;
		}

		@Override
		public Object getTransferData(DataFlavor flavor) throws UnsupportedFlavorException, IOException {
			return cellData;
		}



	}

	//TransferHandler personnalisé pour le Drag&Drop
	public class TransferHelper extends TransferHandler {

		private static final long serialVersionUID = 1L;

		public TransferHelper() {
		}

		@Override
		public int getSourceActions(JComponent c) {
			return MOVE;
		}

		@Override
		protected Transferable createTransferable(JComponent source) {
			// Create the transferable
			JTable table = (JTable) source;
			int row = table.getSelectedRow();
			int col = table.getSelectedColumn();
			Object value = table.getValueAt(row, col);
			return new CellDataTransferable(new CellData(table));
		}

		@Override
		protected void exportDone(JComponent source, Transferable data, int action) {
		}

		@Override
		public boolean canImport(TransferSupport support) {
			// Reject the import by default...
			boolean canImport = false;
			// Can only import into another JTable
			Component comp = support.getComponent();
			if (comp instanceof JTable) {
				JTable target = (JTable) comp;
				// Need the location where the drop might occur
				DropLocation dl = support.getDropLocation();
				Point dp = dl.getDropPoint();
				// Get the column at the drop point
				int dragColumn = target.columnAtPoint(dp);
				try {
					// Get the Transferable, we need to check
					// the constraints
					Transferable t = support.getTransferable();
					CellData cd = (CellData) t.getTransferData(CELL_DATA_FLAVOR);
					// Make sure we're not dropping onto ourselves...
					if (cd.getTable() == target) {
						// Do the columns match...?
						if (dragColumn == cd.getColumn()) {
							canImport = true;
						}
					}
				} catch (UnsupportedFlavorException | IOException ex) {
					ex.printStackTrace();
				}
			}
			return canImport;
		}

		@Override
		public boolean importData(TransferSupport support) {
			// Import failed for some reason...
			boolean imported = false;
			// Only import into JTables...
			Component comp = support.getComponent();
			if (comp instanceof JTable) {
				JTable target = (JTable) comp;
				// Need to know where we are importing to...
				DropLocation dl = support.getDropLocation();
				Point dp = dl.getDropPoint();
				int dropCol = target.columnAtPoint(dp);
				int dropRow = target.rowAtPoint(dp);
				try {
					// Get the Transferable at the heart of it all
					Transferable t = support.getTransferable();
					CellData cd = (CellData) t.getTransferData(CELL_DATA_FLAVOR);
					if (cd.getTable() == target) {
						if (cd.swapValuesWith(dropRow, dropCol)) {
							imported = true;
						}
					}
				} catch (UnsupportedFlavorException | IOException ex) {
					ex.printStackTrace();
				}

			}
			return imported;
		}
	}

	//Cell model personalisé
	public class CellData {
		private final Object value;
		private final int col;
		private final JTable table;
		private final int row;

		public CellData(JTable source) {
			this.col = source.getSelectedColumn();
			this.row = source.getSelectedRow();
			this.value = source.getValueAt(row, col);
			this.table = source;
		}

		public int getColumn() {
			return col;
		}

		public Object getValue() {
			return value;
		}

		public JTable getTable() {
			return table;
		}

		public boolean swapValuesWith(int targetRow, int targetCol) {

			boolean swapped = false;

			if (targetCol == col) {

				Object exportValue = table.getValueAt(targetRow, targetCol);
				table.setValueAt(value, targetRow, targetCol);
				table.setValueAt(exportValue, row, col);
				swapped = true;

			}

			return swapped;

		}

	}

}
