package utils;

import javax.swing.JTable;

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