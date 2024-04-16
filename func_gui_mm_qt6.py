# Author:         Schumann
# Date:           20240415
# Description:    For given one product Description
#                 System will split it by multiple separators and
#                 Then compare it with database records (also being split)
#                 Then return a list shown in a table with higher than a certain similarity %

from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFrame)
from func_db import get_database_config, get_data_from_db_by_sqlString
from func_string import split_string
from PyQt6.QtGui import QGuiApplication


class ProductSimilarity(QDialog):
    def __init__(self, parent=None):
        super(ProductSimilarity, self).__init__(parent)

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
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
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
        # mainLayout.addWidget(self.topLeftGroupBox, 2, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 2, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        # mainLayout.setRowStretch(3, 1)  # Stretch row 3
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Product Name Similarity %")
        self.changeStyle('Fusion')

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

    def calculate_similarity(self, text, products):
        input_strings = split_string(text)
        similarity_scores = []

        for product in products:
            item_id = product[0]
            item_name = product[1]
            product_words = split_string(item_name)
            total_similarity = 0

            for string in input_strings:
                if string in product_words:
                    total_similarity += 1 / len(input_strings)

            similarity_percent = total_similarity * 100
            similarity_scores.append([item_id, item_name, similarity_percent])

        return similarity_scores

    def handleCompareButtonClick(self):
        # Call the function to query the database
        try:
            # Retrieve the product name from the QLineEdit
            product_name = self.lineEntryProductName.text()

            # Calculate the similarity scores
            similarity_scores = self.calculate_similarity(product_name, self.products)

            # Clear the previous results from the result layout
            self.clear_result_layout()

            # Define column count
            column_count = 3

            # Initialize row count
            row = 0

            # Display the new results in the result layout
            for score in similarity_scores:
                # Create QLabel widgets to display the result
                item_id_label = QLabel(str(score[0]))
                item_name_label = QLabel(score[1])
                similarity_percent_label = QLabel("{:.2f}%".format(score[2]))

                print(item_id_label)
                print(item_name_label)
                print(similarity_percent_label)

                # Increment row count
                row += 1

            # Force the scroll area to update its contents
            self.result_widget.update()
        
        except Exception as e:
            print("An exception occurred:", e)

    def createTopSearchGroupBox(self):
        self.topSearchGroupBox = QGroupBox("Search")
        layout = QHBoxLayout()

        self.lineEntryProductName = QLineEdit('')
        self.lineEntryProductName.setEchoMode(QLineEdit.EchoMode.Normal)  # Change echo mode to Normal

        styleLabelProductName = QLabel("&Product Name:")
        styleLabelProductName.setBuddy(self.lineEntryProductName)
        self.lineEntryProductName.setFixedWidth(350) 

        pushButtonSubmit = QPushButton("Compare")
        pushButtonSubmit.setDefault(True)
        pushButtonSubmit.clicked.connect(self.handleCompareButtonClick)

        layout.addWidget(styleLabelProductName)
        layout.addWidget(self.lineEntryProductName)
        layout.addWidget(pushButtonSubmit)
        layout.addStretch(1)
        
        self.topSearchGroupBox.setLayout(layout)
        self.topSearchGroupBox.setFixedHeight(80)


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.CheckState.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        # QTabWidget create tabbed interfaces, where each tab can contain different widgets or content.
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(2, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Comparison Results")
        self.bottomLeftTabWidget.addTab(tab2, "&Explanations")

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

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = ProductSimilarity()
    gallery.show()
    sys.exit(app.exec())