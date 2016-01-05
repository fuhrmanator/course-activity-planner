package ca.etsmtl.activity_planner.utils;

import java.awt.Component;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.EventObject;

import javax.swing.AbstractCellEditor;
import javax.swing.JFormattedTextField;
import javax.swing.JSpinner;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SpinnerDateModel;
import javax.swing.event.CellEditorListener;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.table.TableCellEditor;
import javax.swing.text.DateFormatter;
import javax.swing.text.DefaultFormatterFactory;

import ca.etsmtl.activity_planner.modele.ListeCoursTableModel;

public class SpinnerEditor extends AbstractCellEditor implements TableCellEditor {
	/**
	 *
	 */
	private static final long serialVersionUID = 1L;
	JSpinner spinner = new JSpinner();
	JSpinner.DateEditor editor;
	JTextField textField;
	boolean valueSet;
	SpinnerDateModel model;
	private ListeCoursTableModel tableModel;
	public Date date;

	// Initializes the spinner.
	public SpinnerEditor(SpinnerDateModel model, ListeCoursTableModel tableModel) {

		tableModel = tableModel;
		spinner.setModel(model);

		JFormattedTextField tf = ((JSpinner.DefaultEditor) spinner.getEditor()).getTextField();
		DefaultFormatterFactory factory = (DefaultFormatterFactory) tf.getFormatterFactory();
		DateFormatter formatter = (DateFormatter) factory.getDefaultFormatter();

		// Change the date format to only show the hours
		formatter.setFormat(new SimpleDateFormat("HH:mm"));

	}

	ChangeListener listener = new ChangeListener() {
		  @Override
		public void stateChanged(ChangeEvent e) {

			  tableModel.refreshDeltas(date);
			  fireEditingStopped();
		  }

		};


	@Override
	public Component getTableCellEditorComponent(JTable table, Object value, boolean isSelected, int row, int column) {
		spinner.setValue(value);
		date = (Date) value;
		spinner.addChangeListener(listener);

		return spinner;
	}

	@Override
	public boolean isCellEditable(EventObject evt) {
		return true;
	}

	@Override
	public Object getCellEditorValue() {
		return spinner.getValue();
	}

	@Override
	public void addCellEditorListener(CellEditorListener arg0) {
		// TODO Auto-generated method stub

	}

	@Override
	public void cancelCellEditing() {
		// TODO Auto-generated method stub

	}

	@Override
	public void removeCellEditorListener(CellEditorListener arg0) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean shouldSelectCell(EventObject arg0) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean stopCellEditing() {
		// TODO Auto-generated method stub
		return false;
	}
}
