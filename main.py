from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QMainWindow, QTextEdit
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QFont
from dotenv import load_dotenv
import sys, os
from backend import PlantFinder
import threading

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
PROJECT_ID = 'your_project_id'
 
# Front-End
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plant_finder = PlantFinder(api_key=API_KEY,
                               project_id=PROJECT_ID)  # need to instantiate only once
 
        self.setWindowTitle('Plant Finder')
        self.setMinimumSize(850, 500)  # size of the window 700 px width 500 px height
 
        # Add text area(chat area) widget
        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)
        self.info_area.setFont(QFont("Arial",18))
        self.info_area.setGeometry(30, 30, 650, 400)  # x,y co-ordinates width and height
 
        # Add input field widget
        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont("Arial",18))
        self.input_field.setGeometry(30, 450, 650, 30)
        self.input_field.returnPressed.connect(self.send_message)
 
        # Add Find Button widget
        self.find_button = QPushButton("Find", self)
        self.find_button.setGeometry(700, 450, 100, 30)
        self.find_button.clicked.connect(self.send_message)

        # Add File Selection Button
        self.file_button = QPushButton("Select Image", self)
        self.file_button.setGeometry(700, 400, 100, 30)
        self.file_button.clicked.connect(self.open_file_dialog)

        self.selected_file = None  # Store selected file path

        self.show()


    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Image File", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if file_path:
            self.selected_file = file_path
            self.input_field.setText(file_path)

    def send_message(self):
        user_input = self.input_field.text().strip()
        # append() is a method of QTextEdit()
        self.info_area.append(f"<p style='color:#333333'>File: {user_input}</p>")
        self.input_field.clear()

        thread = threading.Thread(target=self.get_ai_response, args=(user_input, ))
        thread.start()

    def get_ai_response(self, user_input):
        response = self.plant_finder.get_response(user_input)
        self.info_area.append(f"<p style='color:#333333; background-color:#E9E9E9'>Plant Information: {response}</p>")
        #self.info_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        #self.info_area.repaint()
 
app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec())
 
