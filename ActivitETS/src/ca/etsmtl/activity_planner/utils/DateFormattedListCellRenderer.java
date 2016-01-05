package ca.etsmtl.activity_planner.utils;

import java.awt.Component;
import java.text.DateFormat;
import java.util.Date;

import javax.swing.DefaultCellEditor;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JComboBox;
import javax.swing.JList;
import javax.swing.JTable;
import javax.swing.table.TableCellRenderer;

public class DateFormattedListCellRenderer extends DefaultListCellRenderer {

	private DateFormat format;

	public DateFormattedListCellRenderer(DateFormat format) {
		this.format = format;
	}

	@Override
	public Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected,
			boolean cellHasFocus) {
		if (value instanceof Date) {
			value = format.format((Date) value);
		}
		return super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
	}

}