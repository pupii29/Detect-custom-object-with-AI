import sys
import shutil
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QComboBox, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap, QIcon

class YOLOPredictor(QWidget):
    def __init__(self):
        super().__init__()

        self.latest_uploaded_file = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')

        background_label = QLabel(self)
        pixmap = QPixmap('background.png')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        upload_button = QPushButton('Upload File', self)
        upload_button.clicked.connect(self.uploadFile)
        self.stylizeButton(upload_button, '#3498db')

        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems(['calculator', 'wallet'])
        self.stylizeComboBox(self.model_dropdown, '#2ecc71')

        predict_button = QPushButton('Run YOLO Prediction', self)
        predict_button.clicked.connect(self.runYOLOPrediction)
        self.stylizeButton(predict_button, '#e74c3c')

        open_result_button = QPushButton('Open Result File', self)
        open_result_button.clicked.connect(self.openLatestResult)
        self.stylizeButton(open_result_button, '#f39c12')

        layout.addWidget(upload_button)
        layout.addWidget(self.model_dropdown)
        layout.addWidget(predict_button)
        layout.addWidget(open_result_button)

        self.setLayout(layout)

        self.setGeometry(300, 300, pixmap.width(), pixmap.height())
        self.setWindowTitle('IU Lost and Found')
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("background: transparent;")
        self.setStyleSheet("background-color: #ecf0f1;")
        self.show()

    def stylizeButton(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: 2px solid #34495e;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2c3e50;
            }}
        """)

    def stylizeComboBox(self, combo_box, color):
        combo_box.setStyleSheet(f"""
            QComboBox {{
                background-color: {color};
                color: white;
                border: 2px solid #34495e;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QComboBox QAbstractItemView {{
                background-color: {color};
                color: white;
                selection-background-color: #2c3e50;
            }}
        """)

    def uploadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        file_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)")

        if file_path:
            target_directory = r'C:\Users\DELL\anaconda3\envs\yolov8_custom2'

            try:

                shutil.move(file_path, target_directory)
                print(f"File moved to: {target_directory}")

                self.latest_uploaded_file = os.path.join(target_directory, os.path.basename(file_path))
            except Exception as e:
                print(f"Error moving file: {e}")

    def runYOLOPrediction(self):

        self.showNotification("YOLO Prediction", "Running YOLO prediction. Please wait...\nPress OK to continue and wait until the success notification")


        os.environ['CONDA_EXE'] = r'C:\Users\DELL\anaconda3\Scripts\conda.exe'
        os.environ['CONDA_PREFIX'] = r'C:\Users\DELL\anaconda3\envs\yolov8_custom2'
        os.environ['PATH'] = os.pathsep.join([
            os.path.join(os.environ['CONDA_PREFIX'], 'Scripts'),
            os.environ['PATH']
        ])

        uploaded_file = self.latest_uploaded_file

        if uploaded_file:
            selected_model = self.model_dropdown.currentText()

            yolo_command = f'yolo task=detect mode=predict model={selected_model}.pt show=True conf=0.5 source={uploaded_file}'

            try:
                subprocess.run(yolo_command, shell=True, check=True, cwd=r'C:\Users\DELL\anaconda3\envs\yolov8_custom2')
            except subprocess.CalledProcessError as e:
                print(f"Error running YOLO command: {e}")
            finally:

                self.showNotification("YOLO Prediction", "YOLO prediction has finished.\nPress Open Result File to see the result")

    def openLatestResult(self):
        result_folder = r'C:\Users\DELL\anaconda3\envs\yolov8_custom2\runs\detect'

        result_folders = [f for f in os.listdir(result_folder) if os.path.isdir(os.path.join(result_folder, f))]

        if result_folders:
            latest_folder = max(result_folders, key=lambda f: os.path.getmtime(os.path.join(result_folder, f)))

            folder_path = os.path.join(result_folder, latest_folder)
            folder_files = os.listdir(folder_path)

            if folder_files:
                latest_file = max(folder_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

                subprocess.run(['start', os.path.join(folder_path, latest_file)], shell=True)
            else:
                print(f"No files found in the latest folder: {folder_path}")
        else:
            print("No result folders found in the specified directory.")

    def showNotification(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    predictor = YOLOPredictor()
    sys.exit(app.exec_())
