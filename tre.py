import sys
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QListWidget, QLabel, QMessageBox,
                             QProgressBar)
from PyQt6.QtCore import Qt, QTimer

class FileRenamerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # File list
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Selected files and directories:"))
        layout.addWidget(self.file_list)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Files/Directories")
        self.add_button.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)

        self.process_button = QPushButton("Rename Files")
        self.process_button.clicked.connect(self.rename_files)
        button_layout.addWidget(self.process_button)

        layout.addLayout(button_layout)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def add_files(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, False)
        
        if dialog.exec():
            files = dialog.selectedFiles()
            self.file_list.addItems(files)

    def remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def rename_files(self):
        items_to_process = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not items_to_process:
            QMessageBox.warning(self, "No Files", "Please add files or directories to process.")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(items_to_process))
        self.progress_bar.setValue(0)

        self.processed_count = 0
        self.total_count = len(items_to_process)

        self.process_timer = QTimer()
        self.process_timer.timeout.connect(lambda: self.process_next_item(items_to_process))
        self.process_timer.start(0)

    def process_next_item(self, items):
        if self.processed_count < self.total_count:
            item = items[self.processed_count]
            if os.path.isdir(item):
                self.process_directory(item)
            elif os.path.isfile(item):
                self.process_file(item)
            
            self.processed_count += 1
            self.progress_bar.setValue(self.processed_count)
        else:
            self.process_timer.stop()
            self.progress_bar.setVisible(False)
            QMessageBox.information(self, "Process Complete", "File renaming process has finished.")

    def process_directory(self, directory):
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(('.txt', '.md')):
                    file_path = os.path.join(root, filename)
                    self.process_file(file_path)

    def process_file(self, file_path):
        new_name = self.get_new_name_from_file_content(file_path)
        if new_name:
            directory = os.path.dirname(file_path)
            extension = os.path.splitext(file_path)[1]
            new_filepath = os.path.join(directory, new_name + extension)
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(new_filepath):
                new_filepath = os.path.join(directory, f"{new_name}{counter}{extension}")
                counter += 1
            
            print(f"Renaming: {file_path} -> {new_filepath}")
            os.rename(file_path, new_filepath)
            return new_filepath
        else:
            print(f"No title found in: {file_path}")
        return None

    def get_new_name_from_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for _ in range(5):  # Check first 5 lines
                line = file.readline().strip()
                if line.startswith('Title:'):
                    title = line.split(':', 1)[1].strip()
                    if not title:  # If title is on the next line
                        title = file.readline().strip()
                    return self.sanitize_filename(title)
        return None

    def sanitize_filename(self, filename):
        # Remove or replace characters that are invalid in filenames
        return re.sub(r'[<>:"/\\|?*]', '', filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileRenamerGUI()
    window.show()
    sys.exit(app.exec())