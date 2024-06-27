# Author:         Schumann
# Date:           20240424
# Description:    Design the MES Mate Entry

import sys
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,
                             QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget, QMessageBox)
from PyQt6.QtGui import QIcon, QAction, QGuiApplication
from PyQt6.QtCore import QDate
from func_gui_mm_qt6 import ProductSimilarity
from func_gui_mm_ism import ProductSimilarityMulti
from func_gui_mm_ism_long_desc import ProductSimilarityMultiLongDesc
from func.func_db import get_database_config, get_data_from_db_by_sqlString

import pandas as pd
from chart_plotter.combo_chart_by_sql_fields import plot_pool_chart
from data_table_builder.DataTableDialog import DataTableDialog
from datetime import date
from pandas.api.types import is_string_dtype



# 使用QMainWindow创建状态栏。
class MesMate(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # QAction是行为抽象类，包括菜单栏，工具栏，或自定义键盘快捷方式。
        # 在下面的三行中，创建了一个带有特定图标和'Exit'标签的行为。
        # 此外，还为该行为定义了一个快捷方式。
        # 第三行创建一个状态提示，当我们将鼠标指针悬停在菜单项上时，状态栏中就会显示这个提示。
        exitAct = QAction(QIcon('icon\house_go.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+E')
        exitAct.setStatusTip('Exit application')
        # 当选择指定的行为时，触发了一个信号，这个信号连接了QApplication组件的退出操作，这会终止这个应用程序。
        exitAct.triggered.connect(QApplication.instance().quit)

        itemSimSingleAct = QAction(QIcon('icon\drink_empty.png'), '&Item Similarity - Single', self)
        itemSimSingleAct.setShortcut('Ctrl+Shift+S')
        itemSimSingleAct.setStatusTip('Run Item Similarity - Single')
        itemSimSingleAct.triggered.connect(self.show_product_similarity_single)
        # itemSimSingleAct.triggered.connect(self.open_product_similarity)

        itemSimMultiAct = QAction(QIcon('icon\drink.png'), '&Item Similarity - Multiple', self)
        itemSimMultiAct.setShortcut('Ctrl+Shift+M')
        itemSimMultiAct.setStatusTip('Run Item Similarity - Multiple')
        itemSimMultiAct.triggered.connect(self.show_product_similarity_multiple)

        itemSimMultiLongDescAct = QAction(QIcon('icon\drive_magnify.png'), '&Long Description Similarity - Multiple', self)
        itemSimMultiLongDescAct.setShortcut('Ctrl+Shift+L')
        itemSimMultiLongDescAct.setStatusTip('Run Long Description Similarity - Multiple')
        itemSimMultiLongDescAct.triggered.connect(self.show_product_similarity_multiple_long_desc)

        # Call the function to query the database
        config_filename = 'config.json'
        self.config = get_database_config(config_filename)


        # set functional visual area
        self.createCenterTabWidget()

        # Create a central widget and set the layout
        centralWidget = QWidget()
        #  QGridLayout arranges widgets in a grid layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.centerTabWidget, 0, 0)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)




        self.statusBar().showMessage('Ready')
        # menuBar方法创建了一个菜单栏，然后使用addMenu创建一个文件菜单，使用addAction创建一个行为。
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        funcMenu = menubar.addMenu('&Fuctions')
        funcMenu.addAction(itemSimSingleAct)
        funcMenu.addAction(itemSimMultiAct)
        funcMenu.addAction(itemSimMultiLongDescAct)

        margin = 100
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_width = screen_geometry.width() - 2 * margin
        window_height = screen_geometry.height() - 2 * margin

        self.setGeometry(100, 100, window_width, window_height)
        app_icon = QIcon('icon/sport_basketball.png')  # Replace 'icon/app_icon.png' with the path to your icon file
        self.setWindowIcon(app_icon)  # Set the icon using QIcon object
        self.setWindowTitle('MM - Your MES Digital Mate')
        self.show()



    # def open_product_similarity(self):
    #     self.product_similarity_dialog.show()
    #     # Optionally, adjust the position of the dialog within the main window (e.g., using move())

    def show_product_similarity_single(self):
        dialog = ProductSimilarity(self)
        dialog.exec()

    def show_product_similarity_multiple(self):
        dialog = ProductSimilarityMulti(self)
        dialog.exec()

    def show_product_similarity_multiple_long_desc(self):
        dialog = ProductSimilarityMultiLongDesc(self)
        dialog.exec()



    def createCenterTabWidget(self):
        self.centerTabWidget = QTabWidget()
        self.centerTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)

        tabs = ["Planning", "Logistics", "Warehouse", "Procurement", "ME", "Production", "Project"]

        for tab_name in tabs:
            tab = QWidget()
            tab_layout = QVBoxLayout()

            if tab_name == "Production":
                top_row_layout = QHBoxLayout()
                top_row_layout.addWidget(QLabel("Function 1 --->   "))
                top_row_layout.addWidget(QLabel("Pool"))
                # Create QComboBox and populate it with data from stored procedure
                self.combo_box = QComboBox()
                # Add the "ALL_POOLS" option
                self.combo_box.addItem("1001 - All Production Pools")

                pool_results = get_data_from_db_by_sqlString(self.config, "SELECT POOL_ID + ' - ' + POOL_NAME AS POOL_ID FROM UST_PROD_POOL")  # Call the stored procedure
                for row in pool_results:
                    self.combo_box.addItem(row.POOL_ID)  # Assuming the column name is 'pool_id'

                top_row_layout.addWidget(self.combo_box)

                start_label = QLabel("Start")
                self.start_datetime_edit = QDateTimeEdit()
                start_date = QDate.currentDate().addYears(-1)
                self.start_datetime_edit.setDate(start_date)
                self.start_datetime_edit.setDisplayFormat("yyyy-MM-dd")
                top_row_layout.addWidget(start_label)
                top_row_layout.addWidget(self.start_datetime_edit)

                end_label = QLabel("End")
                self.end_datetime_edit = QDateTimeEdit()
                self.end_datetime_edit.setDate(QDate.currentDate())
                self.end_datetime_edit.setDisplayFormat("yyyy-MM-dd")
                top_row_layout.addWidget(end_label)
                top_row_layout.addWidget(self.end_datetime_edit)

                self.commit_button = QPushButton("WO Commit % By Pool")
                self.commit_button.clicked.connect(self.on_commit_button_clicked)
                top_row_layout.addWidget(self.commit_button)

                top_row_layout.addStretch(1)
                tab_layout.addLayout(top_row_layout)

            tab_layout.addStretch()
            tab.setLayout(tab_layout)
            self.centerTabWidget.addTab(tab, f"&{tab_name}")

        self.centerTabWidget.setCurrentIndex(5)

    def on_commit_button_clicked(self):
        selected_pool = self.combo_box.currentText().split()[0]
        pool_id = selected_pool

        data_filepath = "dataset/wo_commit_comparison.csv"

        start_date_qdate = self.start_datetime_edit.date()
        end_date_qdate = self.end_datetime_edit.date()

        # Convert QDate to Python date
        start_date = date(start_date_qdate.year(), start_date_qdate.month(), start_date_qdate.day())
        end_date = date(end_date_qdate.year(), end_date_qdate.month(), end_date_qdate.day())

        pool_data = get_pool_data_from_db(data_filepath, pool_id, start_date, end_date)

        # Check if pool_data is empty
        if pool_data.empty:
            QMessageBox.warning(self, 'Empty Data', 'No production orders for the selected pool.')
        else:
            # Show the data table
            table_dialog = DataTableDialog(pool_data, self)
            table_dialog.exec()

            # Call the plot function from plotter.py
            plot_pool_chart(pool_id, pool_data)


# Pay attention to the data type mismatching issue
def get_pool_data_from_db(data_filepath, pool_id, start_date=None, end_date=None):
    data = pd.read_csv(data_filepath)

    # Convert pool_id to numeric if necessary
    try:
        pool_id = pd.to_numeric(pool_id)
    except ValueError:
        # Handle the case where pool_id cannot be converted to numeric
        print(f"Warning: Unable to convert {pool_id} to numeric")

    if pool_id == 1001:
        pool_data = data  # Keep pool_data as the entire dataset
    else:
        pool_data = data[data['PROD_POOL_ID'] == pool_id]

    # Filter by PROD_COMMITTED date if start_date and end_date are provided
    # Convert PROD_COMMITTED to datetime if it's not already
    if is_string_dtype(pool_data['PROD_COMMITTED']):
        pool_data.loc[:, 'PROD_COMMITTED'] = pd.to_datetime(pool_data['PROD_COMMITTED'])

    if start_date and end_date:
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        pool_data = pool_data[(pool_data['PROD_COMMITTED'] >= start_date) & (pool_data['PROD_COMMITTED'] <= end_date)]

    return pool_data

def main():
    app = QApplication(sys.argv)
    ex = MesMate()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
