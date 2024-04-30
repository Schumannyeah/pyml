# Author:         Schumann
# Date:           20240424
# Description:    Design the MES Mate Entry 

import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon, QAction, QGuiApplication
from func_gui_mm_qt6 import ProductSimilarity
from func_gui_mm_ism import ProductSimilarityMulti


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

        self.statusBar().showMessage('Ready')
        # menuBar方法创建了一个菜单栏，然后使用addMenu创建一个文件菜单，使用addAction创建一个行为。
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        funcMenu = menubar.addMenu('&Fuctions')
        funcMenu.addAction(itemSimSingleAct)
        funcMenu.addAction(itemSimMultiAct)

        margin = 100
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_width = screen_geometry.width() - 2 * margin
        window_height = screen_geometry.height() - 2 * margin

        self.setGeometry(100, 100, window_width, window_height)
        app_icon = QIcon('icon/sport_basketball.png')  # Replace 'icon/app_icon.png' with the path to your icon file
        self.setWindowIcon(app_icon)  # Set the icon using QIcon object
        self.setWindowTitle('MM - Your MES Digital Mate')
        self.show()

        # self.product_similarity_dialog = ProductSimilarity(self)  # Create the dialog instance

    # def open_product_similarity(self):
    #     self.product_similarity_dialog.show()
    #     # Optionally, adjust the position of the dialog within the main window (e.g., using move())

    def show_product_similarity_single(self):
        dialog = ProductSimilarity(self)
        dialog.exec()

    def show_product_similarity_multiple(self):
        dialog = ProductSimilarityMulti(self)
        dialog.exec()


def main():
    app = QApplication(sys.argv)
    ex = MesMate()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
