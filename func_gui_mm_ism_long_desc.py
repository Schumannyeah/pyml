# Author:         Schumann
# Date:           20240425
# Description:    For given batch product descriptions
#                 System will split it by multiple separators and
#                 Then compare it with database records (also being split)
#                 Then return a list shown in a table with higher than a certain similarity %

import pandas as pd
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QWidget, QTableWidgetItem, QFileDialog)
from func.func_db import get_database_config, get_data_from_db_by_sqlString
from func.func_string import split_string
from PyQt6.QtGui import QGuiApplication


class ProductSimilarityMultiLongDesc(QDialog):
    def __init__(self, parent=None):
        super(ProductSimilarityMultiLongDesc, self).__init__(parent)
        self.products = None  # Initialize products attribute
        self.counter = 0  # Initialize counter attribute
        self.counter_previous = 0
        self.counter_populate_table = 0

        #  Create the table widget
        self.tableWidget = QTableWidget()

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())
        styleComboBox.setCurrentText("Fusion")  # Set default selection to "Fusion"

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopSearchGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()

        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        # QHBoxLayout is a layout manager that arranges widgets horizontally from left to right.
        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        # addStretch adds a stretchable space to the layout, which can be used to push widgets towards one end or distribute them evenly within the layout.
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        # control the initial size
        margin = 100
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_width = screen_geometry.width() - 2 * margin
        window_height = screen_geometry.height() - 2 * margin
        self.setFixedSize(window_width, window_height)

        #  QGridLayout arranges widgets in a grid layout
        # adding another layout (topLayout) to it at row 0, column 0, spanning 1 row and 2 columns.
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addWidget(self.topSearchGroupBox, 1, 0)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Long Description Similarity % - Multiple")
        self.changeStyle('Fusion')

        # Set focus to lineEditPercentage
        self.lineEditPercentage.setFocus()

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def calculate_similarity(self, text, products, percentage):
        input_strings = split_string(text.lower())
        similarity_scores = []

        for product in products:
            item_id = product[0]
            item_name_origin = product[1]
            # item_name_lower = product[1].lower()
            long_description = product[2]
            long_description_lower = product[2].lower()
            item_group_id = product[3]
            manufacturer = product[4]
            manufacturer_id = product[5]
            primary_vendor = product[6]
            purchase_price = product[7]
            purchase_stopped = product[8]

            product_words = split_string(long_description_lower)
            total_similarity = 0

            for string in input_strings:
                if string in product_words:
                    total_similarity += 1 / len(input_strings)

            similarity_percent = total_similarity * 100
            if similarity_percent >= percentage:
                similarity_scores.append([item_id, item_name_origin, long_description, item_group_id, manufacturer, 
                                        manufacturer_id, primary_vendor, purchase_price, purchase_stopped, similarity_percent])

            # Sort similarity_scores in descending order based on the similarity percentage
            similarity_scores.sort(key=lambda x: x[3], reverse=True)

        return similarity_scores

    def handleCompareButtonClick(self):
        # Call the function to query the database
        try:
            # Get the text from the QTextEdit in tab2
            tab2 = self.bottomLeftTabWidget.widget(0)  # assuming tab2 is the second widget (index 1)
            text_edit = tab2.findChild(QTextEdit)
            pasted_text = text_edit.toPlainText()
            # Split the pasted text into lines, removing empty spaces
            text_list = [line.strip() for line in pasted_text.splitlines() if line.strip()]
            total_hit_count = 0  # Initialize total hit count

            # Call the function to query the database
            config_filename = 'config.json'
            config = get_database_config(config_filename)
            sqlString = """
                        SELECT	PRODUCT_ID, PRODUCT_NAME, LONG_DESCRIPTION, ITEM_GROUP_ID, 
                                MANUFACTURER, MANUFACTURER_ITEM_ID, 
                                PRIMARY_VENDOR, PURCHASE_PRICE, PURCHASE_STOPPED
                        FROM usv_Ofbiz_ItemTextComparison
                        """
            self.products = get_data_from_db_by_sqlString(config, sqlString)
            # Get the number of columns returned from the database
            num_columns = len(self.products[0]) if self.products else 0

            # Get the table widget from the "Comparison Results" tab
            tableWidget = self.bottomLeftTabWidget.findChild(QTableWidget)
            # before each click, to remove all the content
            self.counter = 0
            self.counter_previous = 0
            self.counter_populate_table = 0

            tableWidget.setRowCount(0)
            tableWidget.repaint()
            # Update the number of columns in the tableWidget
            tableWidget.setColumnCount(num_columns + 1)

            # Iterate through each product name in text_list
            for product_name in text_list:
                # Check if product_name is empty (optional)
                if not product_name:
                    continue

                # Retrieve percentage from lineEditPercentage
                percentage = int(self.lineEditPercentage.text())

                # Calculate similarity scores for this product name
                similarity_scores = self.calculate_similarity(product_name, self.products, percentage)

                # Update hit count for this product
                hit_count = len(similarity_scores)

                # Clear table only for the first product comparison
                if total_hit_count == 0:
                    self.clear_table()

                # Populate table with similarity scores for this product
                self.populate_table(product_name, similarity_scores, tableWidget)

                # Update total hit count and display it
                total_hit_count += hit_count
                self.lineEditHitCount.setText(str(total_hit_count))

            # Set tab2 in focus
            self.bottomLeftTabWidget.setCurrentIndex(1)

        except Exception as e:
            print("An exception occurred:", e)

    def clear_table(self):
        self.tableWidget.clearContents()

    def populate_table(self, product_name, similarity_scores, tableWidget):
        # Set column labels
        tableWidget.setHorizontalHeaderLabels(["SEARCHED TEXT", "SIMILARITY", "PURCHASE STOPPED", "ITEM ID", "ITEM NAME",
                                               "LONG DESCRIPTION","ITEM GROUP ID", "MANUFACTURER", "MANUFACTURER ID",
                                               "PRIMARY VENDOR","PURCHASE PRICE"])

        # Set row count
        self.counter_populate_table += 1
        self.counter_previous = self.counter
        self.counter += len(similarity_scores)  # Increment counter
        # Schumann dated 20240429
        # must setRowCount first for the added data rows
        tableWidget.setRowCount(self.counter)

        # Schumann dated 20240429
        # current_row starting at 0, which shall follow setRowCount
        if self.counter_populate_table == 1:
            current_row = 0
        else:
            current_row = self.counter_previous

        # Iterate through similarity scores and append data to table
        for score in similarity_scores:
            (item_id, item_name, long_description, item_group_id, manufacturer, manufacturer_id,
             primary_vendor, purchase_price, purchase_stopped, similarity_percent) = score

            # Create QTableWidgetItem objects for each cell
            item_searched_text = QTableWidgetItem(product_name)
            similarity_percent_item = QTableWidgetItem("{:.2f}%".format(similarity_percent))
            item_purchase_stopped = QTableWidgetItem(purchase_stopped)
            item_id_item = QTableWidgetItem(str(item_id))
            item_name_item = QTableWidgetItem(item_name)
            item_long_description = QTableWidgetItem(long_description)
            item_group_id_item = QTableWidgetItem(item_group_id)
            item_manufacturer = QTableWidgetItem(manufacturer)
            item_manufacturer_id = QTableWidgetItem(manufacturer_id)
            item_primary_vendor = QTableWidgetItem(primary_vendor)
            item_purchase_price = QTableWidgetItem(str(purchase_price))

            # Append items to the table
            tableWidget.setItem(current_row, 0, item_searched_text)
            tableWidget.setItem(current_row, 1, similarity_percent_item)
            tableWidget.setItem(current_row, 2, item_purchase_stopped)
            tableWidget.setItem(current_row, 3, item_id_item)
            tableWidget.setItem(current_row, 4, item_name_item)
            tableWidget.setItem(current_row, 5, item_long_description)
            tableWidget.setItem(current_row, 6, item_group_id_item)
            tableWidget.setItem(current_row, 7, item_manufacturer)
            tableWidget.setItem(current_row, 8, item_manufacturer_id)
            tableWidget.setItem(current_row, 9, item_primary_vendor)
            tableWidget.setItem(current_row, 10, item_purchase_price)

            # Increment row count for next entry
            current_row += 1

        # Set row count after appending all data (optional)
        # tableWidget.setRowCount(current_row)

        # Adjust column widths to contents (optional)
        tableWidget.resizeColumnsToContents()


    def createTopSearchGroupBox(self):
        self.topSearchGroupBox = QGroupBox("Search")
        layout = QHBoxLayout()

        self.lineEditPercentage = QLineEdit('50')  # Default value is 50
        self.lineEditPercentage.setFixedWidth(50)  # Adjust width as needed

        labelResultOver = QLabel("% Over:")
        labelResultOver.setBuddy(self.lineEditPercentage)

        labelHitCount = QLabel("Hit #:")
        self.lineEditHitCount = QLineEdit()
        self.lineEditHitCount.setReadOnly(True)  # Make it read-only

        pushButtonSubmit = QPushButton("Compare")
        pushButtonSubmit.setDefault(True)
        pushButtonSubmit.clicked.connect(self.handleCompareButtonClick)

        layout.addWidget(labelResultOver)
        layout.addWidget(self.lineEditPercentage)
        layout.addWidget(labelHitCount)
        layout.addWidget(self.lineEditHitCount)
        layout.addWidget(pushButtonSubmit)
        pushButtonExport = QPushButton("Export to Excel")
        pushButtonExport.clicked.connect(self.export_to_excel)
        layout.addWidget(pushButtonExport)
        layout.addStretch(1)
        
        self.topSearchGroupBox.setLayout(layout)
        self.topSearchGroupBox.setFixedHeight(80)

    def createBottomLeftTabWidget(self):
        # QTabWidget create tabbed interfaces, where each tab can contain different widgets or content.
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Ignored)

        tab1 = QWidget()
        # Get the number of columns returned from the database
        num_columns = len(self.products[0]) if self.products else 0
        tableWidget = QTableWidget(0, num_columns)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Paste here multiple lines of text description and one line for one product texts.\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab2, "&Batch Description Input")
        self.bottomLeftTabWidget.addTab(tab1, "&Comparison Results")

        # Set tab2 in focus
        self.bottomLeftTabWidget.setCurrentIndex(0)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
        slider.setValue(80)

        scrollBar = QScrollBar(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(10)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(100)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def export_to_excel(self):
        # Get the table widget from the "Comparison Results" tab
        tableWidget = self.bottomLeftTabWidget.findChild(QTableWidget)

        # Create a DataFrame to store the table data
        data = []
        column_labels = []
        for col in range(tableWidget.columnCount()):
            column_labels.append(tableWidget.horizontalHeaderItem(col).text())
        for row in range(tableWidget.rowCount()):
            row_data = []
            for col in range(tableWidget.columnCount()):
                item = tableWidget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)

        df = pd.DataFrame(data, columns=column_labels)

        # Get the file path to save the Excel file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel file", "", "Excel Files (*.xlsx)")

        if file_path:
            # Export the DataFrame to Excel
            df.to_excel(file_path, index=False)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductSimilarityMultiLongDesc()
    gallery.show()
    sys.exit(app.exec())