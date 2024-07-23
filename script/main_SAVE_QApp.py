import sys
import os
import mimetypes
import docx2txt
from PyPDF2 import PdfReader
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView

def get_file_info(file_path, search_words):
    size = os.path.getsize(file_path)
    file_type = mimetypes.guess_type(file_path)[0]
    word_count = 0
    char_count = 0
    found_words = []

    try:
        content = ""
        if file_type == 'text/plain':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        elif file_type == 'application/pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text()
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = docx2txt.process(file_path)
        elif file_type and file_type.startswith('image/'):
            with Image.open(file_path) as img:
                width, height = img.size
            char_count = width * height  # Total pixels
        
        if content:
            word_count = len(content.split())
            char_count = len(content)
            content_lower = content.lower()
            for word in search_words:
                if word.lower() in content_lower:
                    found_words.append(word)

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

    return size, file_type, word_count, char_count, found_words

class FileInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Root folder input
        root_layout = QHBoxLayout()
        root_layout.addWidget(QLabel('Root Folder:'))
        self.root_input = QLineEdit()
        root_layout.addWidget(self.root_input)
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_folder)
        root_layout.addWidget(browse_button)
        layout.addLayout(root_layout)

        # File names input
        layout.addWidget(QLabel('File Names (comma-separated, leave empty for all):'))
        self.files_input = QLineEdit()
        layout.addWidget(self.files_input)

        # Semantic search input
        layout.addWidget(QLabel('Semantic Search Words (comma-separated):'))
        self.search_input = QLineEdit()
        layout.addWidget(self.search_input)

        # Execute button
        execute_button = QPushButton('Execute')
        execute_button.clicked.connect(self.execute)
        layout.addWidget(execute_button)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels(['Filename', 'File Path', 'Size', 'File Type', 'Word Count', 'Char Count', 'Found Words'])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)

        self.setLayout(layout)
        self.setWindowTitle('File Info App')
        self.setGeometry(300, 300, 1000, 600)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Root Folder")
        if folder:
            self.root_input.setText(folder)

    def execute(self):
        root_folder = self.root_input.text()
        file_names = [name.strip() for name in self.files_input.text().split(',')] if self.files_input.text() else []
        search_words = [word.strip() for word in self.search_input.text().split(',')] if self.search_input.text() else []

        results = []
        for foldername, subfolders, filenames in os.walk(root_folder):
            for filename in filenames:
                if not file_names or filename in file_names:
                    file_path = os.path.join(foldername, filename)
                    size, file_type, word_count, char_count, found_words = get_file_info(file_path, search_words)
                    results.append((filename, file_path, size, file_type, word_count, char_count, ', '.join(found_words)))

        self.display_results(results)

    def display_results(self, results):
        self.results_table.setRowCount(len(results))
        for row, result in enumerate(results):
            for col, value in enumerate(result):
                item = QTableWidgetItem(str(value))
                self.results_table.setItem(row, col, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileInfoApp()
    ex.show()
    sys.exit(app.exec_())