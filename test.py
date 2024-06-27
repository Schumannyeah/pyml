# Author:         Schumann
# Date:           20240424
# Description:    Design the MES Mate Entry

import sys
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,
                             QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QTabWidget, QVBoxLayout, QWidget, QMessageBox)
from PyQt6.QtGui import QIcon, QAction, QGuiApplication
from PyQt6.QtCore import QDate
from func_gui_mm_qt6 import ProductSimilarity
from func_gui_mm_ism import ProductSimilarityMulti
from func_gui_mm_ism_long_desc import ProductSimilarityMultiLongDesc
from func.func_db import get_database_config, execute_stored_procedure, get_data_from_db_by_sqlString

import pandas as pd
import json
from chart_plotter.combo_chart_by_sql_fields import plot_combo_chart, plot_scatter_chart, plot_distribution_chart
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

        # Load the JSON data from the config file
        with open('config.json', 'r') as file:
            config_data = json.load(file)

        # Retrieve the value of "main_screen_margin"
        main_screen_margin = config_data.get('main_screen_margin')

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

        margin = main_screen_margin
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_width = screen_geometry.width() - 2 * margin
        window_height = screen_geometry.height() - 2 * margin

        self.setGeometry(main_screen_margin, main_screen_margin, window_width, window_height)
        app_icon = QIcon('icon/sport_basketball.png')  # Replace 'icon/app_icon.png' with the path to your icon file
        self.setWindowIcon(app_icon)  # Set the icon using QIcon object
        self.setWindowTitle('MM - Your MES Digital Mate')
        self.show()

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
            tab_layout_production = QVBoxLayout()

            if tab_name == "Production":
                top_row_layout_production = QHBoxLayout()

                # Function 1
                top_row_layout_production.addWidget(QLabel("Function 1 --->   "))
                top_row_layout_production.addWidget(QLabel("Pool"))
                # Create QComboBox and populate it with data from stored procedure
                self.combo_box_pool = QComboBox()
                self.combo_box_pool.addItem("1001 - All Production Pools")

                pool_results = get_data_from_db_by_sqlString(self.config, "SELECT POOL_ID + ' - ' + POOL_NAME AS POOL_ID FROM UST_PROD_POOL")  # Call the stored procedure
                for row in pool_results:
                    self.combo_box_pool.addItem(row.POOL_ID)  # Assuming the column name is 'pool_id'

                top_row_layout_production.addWidget(self.combo_box_pool)

                label_start = QLabel("Start")
                self.start_datetime_edit = QDateTimeEdit()
                start_date = QDate.currentDate().addYears(-1)
                self.start_datetime_edit.setDate(start_date)
                self.start_datetime_edit.setDisplayFormat("yyyy-MM-dd")
                top_row_layout_production.addWidget(label_start)
                top_row_layout_production.addWidget(self.start_datetime_edit)

                label_end = QLabel("End")
                self.end_datetime_edit = QDateTimeEdit()
                self.end_datetime_edit.setDate(QDate.currentDate())
                self.end_datetime_edit.setDisplayFormat("yyyy-MM-dd")
                top_row_layout_production.addWidget(label_end)
                top_row_layout_production.addWidget(self.end_datetime_edit)

                self.button_wo_commit = QPushButton("WO Commit % By Pool")
                self.button_wo_commit.clicked.connect(self.on_wo_commit_button_clicked)
                top_row_layout_production.addWidget(self.button_wo_commit)

                top_row_layout_production.addStretch(1)
                tab_layout_production.addLayout(top_row_layout_production)

                # Function 2
                sec_row_layout_production = QHBoxLayout()
                sec_row_layout_production.addWidget(QLabel("Function 2 --->   "))

                sec_row_layout_production.addWidget(QLabel("Function Category"))
                # Create QComboBox and populate it with data from stored procedure
                self.combo_box_func_lt_comp_cat = QComboBox()
                self.combo_box_func_lt_comp_cat.addItem("Product LeadTime Delta By Week")
                self.combo_box_func_lt_comp_cat.addItem("WO LeadTime Delta Distribution By Days")
                self.combo_box_func_lt_comp_cat.addItem("WO LeadTime Delta Scatter By Days")
                sec_row_layout_production.addWidget(self.combo_box_func_lt_comp_cat)

                sec_row_layout_production.addWidget(QLabel("Product Category"))
                # Create QComboBox and populate it with data from stored procedure
                self.combo_box_prod_cat = QComboBox()
                self.combo_box_prod_cat.addItem("AX_All")
                self.combo_box_prod_cat.addItem("AX_NA")

                prod_cat_results = get_data_from_db_by_sqlString(self.config,
                                    "select PRODUCT_CATEGORY_ID from PRODUCT_CATEGORY where product_category_id like 'AX_%'")
                for row in prod_cat_results:
                    self.combo_box_prod_cat.addItem(row.PRODUCT_CATEGORY_ID)  # Assuming the column name is 'pool_id'

                sec_row_layout_production.addWidget(self.combo_box_prod_cat)

                label_past_days = QLabel("Past Days")
                self.lineEntryPastDays = QLineEdit('')
                self.lineEntryPastDays.setEchoMode(QLineEdit.EchoMode.Normal)
                self.lineEntryPastDays.setFixedWidth(100)
                sec_row_layout_production.addWidget(label_past_days)
                sec_row_layout_production.addWidget(self.lineEntryPastDays)

                self.button_product_lt_vs_actual = QPushButton("Product LT Vs Actual By Cateogry")
                self.button_product_lt_vs_actual.clicked.connect(self.on_product_lt_vs_actual_button_clicked)
                sec_row_layout_production.addWidget(self.button_product_lt_vs_actual)

                sec_row_layout_production.addStretch(1)
                tab_layout_production.addLayout(sec_row_layout_production)


            # this forces elements to align from left
            tab_layout_production.addStretch()
            tab.setLayout(tab_layout_production)
            self.centerTabWidget.addTab(tab, f"&{tab_name}")

        self.centerTabWidget.setCurrentIndex(5)

    def on_wo_commit_button_clicked(self):
        selected_pool = self.combo_box_pool.currentText().split()[0]
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
            plot_combo_chart(pool_data, pool_id, 'WO_END_YM', 'NUMERATOR_ACTUAL',
                             'WO COMMIT')

    def on_product_lt_vs_actual_button_clicked(self):
        selected_prod_cat = self.combo_box_prod_cat.currentText().split()[0]
        prod_cat = selected_prod_cat

        selected_func_lt_comp_cat = self.combo_box_func_lt_comp_cat.currentText()
        func_lt_comp_cat = selected_func_lt_comp_cat

        sp_name = ""
        if func_lt_comp_cat == "Product LeadTime Delta By Week":
            sp_name = "usp_Ofbiz_PP_ProductLTDeltaByWeek"
        elif func_lt_comp_cat == "WO LeadTime Delta Distribution By Days":
            sp_name = "usp_Ofbiz_PP_CompareEndWoLtWithProdLtByPastDays"
        elif func_lt_comp_cat == "WO LeadTime Delta Scatter By Days":
            sp_name = "usp_Ofbiz_PP_CompareEndWoLtWithProdLtByPastDays"

        sp_name = sp_name + " " + self.lineEntryPastDays.text()
        data_product_lt_vs_actual = execute_stored_procedure(self.config, sp_name)

        # Convert the result to a pandas DataFrame if it is a list of dictionaries
        if isinstance(data_product_lt_vs_actual, list):
            data_product_lt_vs_actual = pd.DataFrame(data_product_lt_vs_actual)

        # Check if pool_data is empty
        if data_product_lt_vs_actual.empty:
            QMessageBox.warning(self, 'Empty Data', 'No production orders for the selected pool.')
        else:
            data_product_lt_vs_actual = filter_data(data_product_lt_vs_actual, PRODUCT_CATEGORY=prod_cat)
            # Show the data table
            table_dialog = DataTableDialog(data_product_lt_vs_actual, self)
            table_dialog.exec()

            # Call the plot function from plotter.py
            if func_lt_comp_cat == "Product LeadTime Delta By Week":
                plot_scatter_chart(data_product_lt_vs_actual, 'LT_IN_WEEK', 'LT_DEV_IN_WEEK'
                                   'Deviation Lead Time In Week Scatter By Product LT In Week')
            elif func_lt_comp_cat == "WO LeadTime Delta Distribution By Days":
                plot_distribution_chart(data_product_lt_vs_actual, 'LT_DEV', 'WO_POOL_ID',
                                        "Distribution of Lead Time Deviation By Pool")
            elif func_lt_comp_cat == "WO LeadTime Delta Scatter By Days":
                plot_scatter_chart(data_product_lt_vs_actual, 'WO_LT', 'LT_DEV',
                                        "Deviation Lead Time Scatter In Days By WO Actual Run LT In Days")


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

# filtering data
def filter_data(data, *args, **kwargs):
    # print(f"Fixed argument (data): {data}")

    # Count and print the positional arguments
    # print(f"Number of positional arguments: {len(args)}")
    for i, arg in enumerate(args):
        print(f"Positional argument {i + 1}: {arg} (type: {type(arg)})")

    # Count and print the keyword arguments
    print(f"Number of keyword arguments: {len(kwargs)}")
    for key, value in kwargs.items():
        print(f"Keyword argument '{key}': {value} (type: {type(value)})")
        if key == 'PRODUCT_CATEGORY':
            if value == 'AX_All':
                data_returned = data
            else:
                data_returned = data[data['PRODUCT_CATEGORY'] == value]

    return data_returned


def main():
    app = QApplication(sys.argv)
    ex = MesMate()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
