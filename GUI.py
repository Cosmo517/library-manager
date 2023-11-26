from database_queries import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, \
    QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        q_btn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel('One or more of the text fields are empty. Please fill them')
        custom_font = message.font()
        custom_font.setPointSize(11)
        message.setFont(custom_font)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def closeEvent(self, event):
        self.con.close()

    @staticmethod
    def create_line_edits(placeholder_text):
        temp_edit = QLineEdit()
        temp_edit.setPlaceholderText(placeholder_text)
        return temp_edit

    def create_table(self):
        item = QTableWidgetItem()
        all_books = get_all_rows(self.con)
        rows = 0
        for i in all_books:
            for j in range(0, 9):
                item.setText("test")
                # FIXME: not workign for some reason...
                self.table_widget.setItem(self.table_widget.rowCount() + rows, j, item)
            rows = rows + 1

    def __init__(self):
        super().__init__()

        # TODO: Change later so user can choose database
        #  from the GUI, rather than having to type in the name
        self.con, self.database_name = create_database_connection()
        database_setup(self.con)
        print(get_all_rows(self.con))

        self.setWindowTitle("Library Manager")

        # Create Page layout
        page_layout = QVBoxLayout()

        # create the text boxes
        self.line_edits = [self.create_line_edits("Book Name"), self.create_line_edits("Author Name"),
                           self.create_line_edits("Volume Number"), self.create_line_edits("Page Count"),
                           self.create_line_edits("Rating"), self.create_line_edits("Own"),
                           self.create_line_edits("Read"),
                           self.create_line_edits("Genre"), self.create_line_edits("Cover Type")]

        for i in self.line_edits:
            page_layout.addWidget(i)

        # Create Add Book Button
        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_button_interaction)
        page_layout.addWidget(self.add_button)

        # create table widget
        self.table_widget = QTableWidget(get_count_of_rows(self.con)+10, 9)
        headers = ['Book Name', 'Volume', 'Author Name', 'Page Count',
                   'Rating', 'Own', 'Read', 'Genre', 'Cover Type']
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.create_table()
        page_layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(page_layout)
        self.setCentralWidget(container)

    def add_button_interaction(self):
        if any(i.text() == '' for i in self.line_edits):
            dlg = CustomDialog()
            dlg.exec()
            return
        strings = []
        for i in self.line_edits:
            strings.append(i.text())
        insert_into_table(self.con, strings[0], strings[2], strings[1],
                          strings[3], strings[4], strings[5], strings[6],
                          strings[7], strings[8])
        for i in self.line_edits:
            i.clear()


def setup_application():
    # create application instance
    app = QApplication([])
    # create widget
    window = MainWindow()
    # windows are invisible by default
    window.show()
    app.exec()
