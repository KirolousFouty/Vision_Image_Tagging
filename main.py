import sys
import os
import subprocess
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QDialog, QLabel, QTextEdit
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minimalist GUI")
        self.resize(300, 200)
        self.center()

        self.create_folders()
        self.create_tags_file()

        layout = QVBoxLayout()

        self.input_button = QPushButton("Open Input Folder")
        self.input_button.clicked.connect(self.open_input_folder)
        layout.addWidget(self.input_button)

        self.output_button = QPushButton("Open Output Folder")
        self.output_button.clicked.connect(self.open_output_folder)
        layout.addWidget(self.output_button)

        self.process_button = QPushButton("Process Current Input")
        self.process_button.clicked.connect(self.process_input)
        layout.addWidget(self.process_button)

        self.search_button = QPushButton("Search by Tag")
        self.search_button.clicked.connect(self.search_by_tag)
        layout.addWidget(self.search_button)

        self.show_tags_button = QPushButton("Show All Tags")
        self.show_tags_button.clicked.connect(self.show_all_tags)
        layout.addWidget(self.show_tags_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_gm.moveCenter(screen)
        self.move(frame_gm.topLeft())

    def create_folders(self):
        if not os.path.exists("input"):
            os.makedirs("input")
        if not os.path.exists("output"):
            os.makedirs("output")

    def create_tags_file(self):
        if not os.path.exists("tags.csv"):
            with open("tags.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tag"])  # Writing a header for the CSV file

    def open_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        folder_path = os.path.abspath(folder_name)
        if sys.platform == "win32":
            os.startfile(folder_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder_path])
        else:
            subprocess.Popen(["xdg-open", folder_path])

    def open_input_folder(self):
        self.create_folders()
        self.open_folder("input")

    def open_output_folder(self):
        self.create_folders()
        self.open_folder("output")

    def process_input(self):
        script_path = os.path.abspath("script.py")
        if os.path.exists(script_path):
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            self.show_process_output(output)
        else:
            QMessageBox.warning(self, "Process Input", "script.py not found!")

    def show_process_output(self, output):
        dialog = QDialog(self)
        dialog.setWindowTitle("Process Output")
        dialog.resize(400, 300)

        layout = QVBoxLayout()

        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setPlainText(output)
        layout.addWidget(output_text)

        dialog.setLayout(layout)
        dialog.exec_()

    def search_by_tag(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Search by Tag")
        dialog.resize(300, 150)

        layout = QVBoxLayout()

        label = QLabel('Write tags separated by "OR" or separated by "AND"')
        layout.addWidget(label)

        self.tag_input = QLineEdit()
        layout.addWidget(self.tag_input)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def perform_search(self):
        tags = self.tag_input.text()
        # Placeholder for search logic
        QMessageBox.information(self, "Search by Tag", f"Searching for tags: {tags}")

    def show_all_tags(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("All Tags")
        dialog.resize(300, 200)

        layout = QVBoxLayout()

        tags_text = QTextEdit()
        tags_text.setReadOnly(True)
        layout.addWidget(tags_text)

        tags = self.get_all_tags()
        tags_text.setPlainText("\n".join(tags))

        dialog.setLayout(layout)
        dialog.exec_()

    def get_all_tags(self):
        tags = []
        if os.path.exists("tags.csv"):
            with open("tags.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                tags = [row[0] for row in reader]
        return tags

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
