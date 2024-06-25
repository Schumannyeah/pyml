from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QMenu, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import pandas as pd

class DataTableDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data Table")
        self.setGeometry(120, 150, 1200, 650)

        layout = QVBoxLayout(self)
        # Reset index to ensure correct display in the table
        data = data.reset_index(drop=True)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(data.shape[0])
        self.tableWidget.setColumnCount(data.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(data.columns)

        # data.iterrows(): is a pandas function that allows iteration over DataFrame Rows as
        # (index, series) pairs, 'row_index' is the index of the row in the DataFrame
        # 'row' is a pandas Series object containing the data for that row.
        for row_index, row in data.iterrows():
            # enumerate(row): allows iteration over the values in the 'row' Series, providing
            # both column index ('col_index') and the value ('value')
            # 'col_index' is the index of the column in the DataFrame
            # 'value' is the actual cell located at ('row_index', 'col_index')
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.createContextMenu()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        exportAction = QAction('Export as Excel', self)
        exportAction.triggered.connect(self.exportAsExcel)

        self.addAction(exportAction)

    def exportAsExcel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data as Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                # Retrieve data from tableWidget
                num_rows = self.tableWidget.rowCount()
                num_cols = self.tableWidget.columnCount()

                data = []
                for row in range(num_rows):
                    row_data = []
                    for col in range(num_cols):
                        item = self.tableWidget.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    data.append(row_data)

                # Convert data to DataFrame
                df = pd.DataFrame(data, columns=[self.tableWidget.horizontalHeaderItem(col).text() for col in
                                                 range(num_cols)])

                # Save DataFrame to Excel
                df.to_excel(file_name, index=False)

                QMessageBox.information(self, 'Export Successful', 'Data exported successfully.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to export data: {str(e)}')
        else:
            # Workaround to keep context menu open after canceling the file dialog
            self.showContextMenu()

    def showContextMenu(self):
        menu = QMenu(self)
        exportAction = QAction('Export as Excel', self)
        exportAction.triggered.connect(self.exportAsExcel)
        menu.addAction(exportAction)
        menu.exec(self.mapToGlobal(self.tableWidget.viewport().rect().center()))