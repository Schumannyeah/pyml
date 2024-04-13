import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from func_string import split_string
from func_db import get_database_config, get_data_from_db_by_sqlString


class TextSimilarityCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Get the screen geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculate the window size with margins
        margin = 100
        window_width = screen_geometry.width() - 2 * margin
        window_height = screen_geometry.height() - 2 * margin

        self.setWindowTitle("Product Name Similarity Calculator")
        self.setGeometry(margin, margin, window_width, window_height)        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a horizontal layout for the input row
        input_row_layout = QHBoxLayout()
        input_row_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align layout to the left and top

        # Create the input label
        self.input_label = QLabel("Product Name:")
        self.input_label.setFixedSize(100, 40)  # Set size of the input label
        input_row_layout.addWidget(self.input_label)

        # Create the entry widget
        self.entry = QLineEdit()
        self.entry.setFixedSize(400, 40)  # Set size of the entry widget
        input_row_layout.addWidget(self.entry)

        # Create the submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(100, 40)  # Set size of the submit button
        self.submit_button.clicked.connect(self.on_submit)
        input_row_layout.addWidget(self.submit_button)

        layout.addLayout(input_row_layout)

        # Create a scroll area for the result layout
        result_scroll_area = QScrollArea()
        result_scroll_area.setWidgetResizable(True)

        # Create a widget to contain the result layout
        self.result_widget = QWidget()  # Define result_widget as an attribute
        self.result_layout = QVBoxLayout(self.result_widget)  # Define result_layout as an attribute

        # Set the widget as the content of the scroll area
        result_scroll_area.setWidget(self.result_widget)

        layout.addWidget(result_scroll_area)

        self.setLayout(layout)
        

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

    def on_submit(self):
        # Get the text from the entry widget
        text = self.entry.text()

        # Calculate the similarity scores
        similarity_scores = self.calculate_similarity(text, self.products)

        # Clear the previous results from the result layout
        self.clear_result_layout()

        # Display the new results in the result layout
        for score in similarity_scores:
            # Create QLabel widgets to display the result
            item_id_label = QLabel(str(score[0]))
            item_name_label = QLabel(score[1])
            similarity_percent_label = QLabel("{:.2f}%".format(score[2]))

            # Append the labels to a list
            # labels = [item_id_label, item_name_label, similarity_percent_label]

            # Add the labels to the result layout
            # for label in labels:
            #     self.result_layout.addWidget(label)

            # Add the labels to the result layout
            self.result_layout.addWidget(item_id_label, row, 0 % column_count)
            self.result_layout.addWidget(item_name_label, row, 1 % column_count)
            self.result_layout.addWidget(similarity_percent_label, row, 2 % column_count)

        # Force the scroll area to update its contents
        self.result_widget.update()



    def clear_result_layout(self):
        # Remove all widgets from the grid layout
        for i in reversed(range(self.result_layout.count())):
            self.result_layout.itemAt(i).widget().setParent(None)


def main():
    app = QApplication(sys.argv)
    window = TextSimilarityCalculator()

    config_filename = 'config.json'
    config = get_database_config(config_filename)
    sqlString = "select top 100 ITEM_ID, ITEM_NAME from usv_Ax_InventTable"
    window.products = get_data_from_db_by_sqlString(config, sqlString)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
