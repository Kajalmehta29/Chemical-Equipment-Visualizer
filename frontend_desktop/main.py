import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QLineEdit, QFrame, QMessageBox, QScrollArea, QListWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/"

STYLESHEET = """
QWidhet{
color: #333333;
}
QMainWindow {
    background-color: white; 
}
QFrame#Card {
    background-color: white;
    border-radius: 8px;
    border: 1px solid #d0d0d0; 
}
QLabel {
    color: #333333; 
}
QLabel#Header {
    font-size: 24px;
    color: #2c3e50;
    font-weight: bold;
    margin-bottom: 5px;
}
QLabel#SubHeader {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 20px;
}
QLabel#SectionTitle {
    font-size: 16px;
    color: #008080;
    font-weight: bold;
    padding-bottom: 5px;
    border-bottom: 2px solid #eee;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 14px;
    background-color: #fafafa;
    color: #333333;
}
QListWidget {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: #fafafa;
    font-size: 13px;
    color: #333333;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #eee;
}
QListWidget::item:selected {
    background-color: #e0f2f1; 
    color: #004d40;
}
QPushButton {
    background-color: #008080;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #006666;
}
"""

class ChemicalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1100, 750)
        self.setStyleSheet(STYLESHEET)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget) 

        self.left_panel = QVBoxLayout()
        self.left_panel.setAlignment(Qt.AlignTop)
        
        # Header
        self.lbl_title = QLabel("Chemical Visualizer")
        self.lbl_title.setObjectName("Header")
        self.left_panel.addWidget(self.lbl_title)
        
        self.create_auth_card()
        self.create_history_card()
        
        self.main_layout.addLayout(self.left_panel, 1) 

        self.right_panel = QVBoxLayout()
        self.create_stats_card()
        self.main_layout.addLayout(self.right_panel, 2) 

        self.refresh_history()

    def create_auth_card(self):
        self.auth_frame = QFrame()
        self.auth_frame.setObjectName("Card")
        layout = QVBoxLayout(self.auth_frame)
        
        layout.addWidget(QLabel("Data Upload", objectName="SectionTitle"))

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Username (admin)")
        layout.addWidget(self.txt_user)
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Password")
        self.txt_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.txt_pass)

        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(self.btn_upload)
        
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(self.lbl_status)
        
        self.left_panel.addWidget(self.auth_frame)

    def create_history_card(self):
        self.hist_frame = QFrame()
        self.hist_frame.setObjectName("Card")
        layout = QVBoxLayout(self.hist_frame)
        
        layout.addWidget(QLabel("Recent History", objectName="SectionTitle"))
        
        self.list_history = QListWidget()
        self.list_history.itemClicked.connect(self.load_history_item)
        layout.addWidget(self.list_history)

        self.left_panel.addWidget(self.hist_frame)

    def create_stats_card(self):
        self.stats_frame = QFrame()
        self.stats_frame.setObjectName("Card")
        self.stats_frame.hide() 
        layout = QVBoxLayout(self.stats_frame)

        # Title with Filename
        self.lbl_stats_title = QLabel("Analysis Results")
        self.lbl_stats_title.setObjectName("SectionTitle")
        layout.addWidget(self.lbl_stats_title)

        # Text Stats
        self.lbl_total = QLabel()
        self.lbl_total.setFont(QFont("Arial", 14))
        layout.addWidget(self.lbl_total)
        
        self.lbl_averages = QLabel()
        self.lbl_averages.setFont(QFont("Arial", 12))
        self.lbl_averages.setStyleSheet("color: #34495e; line-height: 150%;")
        layout.addWidget(self.lbl_averages)

        # Chart
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.right_panel.addWidget(self.stats_frame)

    def get_auth(self):
        return (self.txt_user.text(), self.txt_pass.text())

    def refresh_history(self):
        try:
            response = requests.get(f"{API_URL}history/")
            if response.status_code == 200:
                self.list_history.clear()
                self.history_data = response.json()
                for item in self.history_data:
                    display_text = f"📄 {item['filename']}\n   {item['uploaded_at'][:10]}"
                    self.list_history.addItem(display_text)
        except:
            pass 

    def load_history_item(self, item):
        row = self.list_history.row(item)
        file_id = self.history_data[row]['id']
        username, password = self.get_auth()
        
        if not username or not password:
             QMessageBox.warning(self, "Auth Required", "Please enter credentials to view details.")
             return

        try:
            response = requests.get(f"{API_URL}history/{file_id}/", auth=(username, password))
            if response.status_code == 200:
                self.update_ui(response.json())
            else:
                QMessageBox.warning(self, "Error", "Could not load data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def upload_file(self):
        username, password = self.get_auth()
        if not username or not password:
            QMessageBox.warning(self, "Auth Error", "Please enter username and password.")
            return

        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', filter="CSV Files (*.csv)")
        if fname:
            self.lbl_status.setText("Uploading...")
            files = {'file': open(fname, 'rb')}
            try:
                response = requests.post(f"{API_URL}upload/", files=files, auth=(username, password))
                if response.status_code == 201:
                    data = response.json()
                    self.update_ui(data)
                    self.lbl_status.setText("Upload Complete")
                    self.refresh_history()
                elif response.status_code == 401:
                    self.lbl_status.setText("Login Failed")
                    QMessageBox.critical(self, "Error", "Invalid Credentials")
                else:
                    self.lbl_status.setText(f"Error: {response.status_code}")
            except Exception as e:
                self.lbl_status.setText("Connection Failed")

    def update_ui(self, data):
        self.stats_frame.show()
        
        # Update Title
        filename = data.get('filename', 'Unknown File')
        self.lbl_stats_title.setText(f"Analysis Results: {filename}")
        
        # Update Text
        self.lbl_total.setText(f"Total Equipment Count: {data.get('total_count', 0)}")
        
        avgs = data.get('averages', {})
        avg_text = "\nParameter Averages:\n"
        for key, val in avgs.items():
            avg_text += f"• {key}: {val:.2f}\n"
        self.lbl_averages.setText(avg_text)

        # Update Chart
        self.ax.clear()
        dist = data.get('type_distribution', {})
        if dist:
            colors = ['#008080', '#2c3e50', '#f1c40f', '#e74c3c'] 
            self.ax.bar(dist.keys(), dist.values(), color=colors[:len(dist)])
            self.ax.set_title("Equipment Type Distribution")
            self.ax.set_ylabel("Count")
            self.ax.tick_params(axis='x', labelsize=8)
            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChemicalApp()
    window.show()
    sys.exit(app.exec_())