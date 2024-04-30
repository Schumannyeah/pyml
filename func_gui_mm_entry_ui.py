# Author:         Schumann
# Date:           20240424
# Description:    Design the MES Mate Entry 


from PyQt6 import uic
# from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu
from PyQt6.QtGui import QAction
# Importing ProductSimilarity from func_gui_mm_qt6 module


from func_gui_mm_qt6 import ProductSimilarity

Form, Window = uic.loadUiType("mm_entry.ui")

# app = QApplication([])
# window = Window()
# form = Form()
# form.setupUi(window)
# window.show()
# app.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.ui = Form()
        self.ui.setupUi(self)

        # # Accessing the menu bar from the central widget
        # menubar = self.ui.centralwidget.findChild(QMenuBar, "menubar")
        # if not menubar:
        #     print("Menu bar not found in the UI.")
        #     return
        
        # Accessing the menu bar of the main window
        menubar = self.menuBar()

        # Accessing the specific menu by its object name
        menu_functions = menubar.findChild(QMenu, "menuFunctions")
        if not menu_functions:
            print("Menu 'Functions' not found.")
            return

        # # Accessing the menu bar of the main window
        # menubar = self.menuBar()

        # # Adding a menu to the menu bar
        # menu = menubar.addMenu("Menu")

        print("Starting Printing")
        
        # Find the action by object name
        self.action_item_similarity_single = menu_functions.findChild(QAction, "actionItem_Similarity_Single")
        if self.action_item_similarity_single:  # Check if action found
            self.action_item_similarity_single.triggered.connect(self.show_product_similarity)  # Connect signal to slot
        else:
            print("Action 'Item Similarity - Single' not found in the UI.")



        # # Create actions for menu items
        # action_item_single = QAction("Item Similarity - Single", self)
        # action_item_single.setObjectName("actionItem_Similarity_Single")  # Set object name
        # action_item_single.triggered.connect(self.show_product_similarity)

        # Add actions to the menu
        # menu_functions.addAction(action_item_single)

    def show_product_similarity(self):
        print("You are here")
        dialog = ProductSimilarity(self)
        dialog.exec()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())