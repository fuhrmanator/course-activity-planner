package ca.etsmtl.activity_planner.utils;

import java.awt.Color;
import java.awt.Component;

import javax.swing.JTable;
import javax.swing.table.DefaultTableCellRenderer;;

public class TableRenderer extends DefaultTableCellRenderer {

	public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus,
			int row, int column) {
		Component cell = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
			
			if(row % 2 == 0) {
				cell.setBackground(Color.LIGHT_GRAY);
			} else {
				cell.setBackground(Color.white);
			}
			
		return cell;
	}
}