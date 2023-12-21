import sys
import os
import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QProgressBar, QLineEdit
from PyQt5.QtCore import Qt, QTimer
import requests

class MyPopup(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setText(message)

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.url_to_verify = ""

        self.setup_interface()

    def setup_interface(self):
        self.setWindowTitle('URL Verifier')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel('Status: Waiting...')
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.input_url = QLineEdit(self)
        self.input_url.setPlaceholderText("Enter the URL to verify")
        layout.addWidget(self.input_url)

        self.start_button = QPushButton('Start Verification')
        self.start_button.clicked.connect(self.start_verification)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def show_popup(self, message):
        popup = MyPopup(message)
        popup.exec_()

    def get_page_content(self, url):
        try:
            response = requests.get(url)
            return response.status_code, response.text  # Changed to response.text
        except requests.exceptions.ConnectionError:
            return 'Connection Error', None

    def perform_verification_until_200(self, wait_minutes):
        countdown_seconds = wait_minutes * 60
        update_interval = 1000  # milliseconds

        self.progress_bar.setRange(0, countdown_seconds)
        self.progress_bar.setValue(0)

        while True:
            status_code, content = self.get_page_content(self.url_to_verify)
            current_time = datetime.datetime.now()
            self.status_label.setText(f'Last request made at: {current_time}')

            if status_code == 200:
                self.show_popup('Success! Code 200 reached')
                break
            else:
                for remaining_seconds in range(countdown_seconds):
                    self.progress_bar.setValue(remaining_seconds)
                    self.status_label.setText(
                        f'Status Code: {status_code}\nLast request made at: {current_time}')
                    time.sleep(1)
                    QApplication.processEvents()

                self.status_label.setText(f'Retrying in {wait_minutes} minutes...')
                self.progress_bar.setValue(0)
                time.sleep(wait_minutes * 60)

        self.show_popup('Process completed.')

    def start_verification(self):
        self.url_to_verify = self.input_url.text()
        if not self.url_to_verify:
            self.show_popup('Please enter a valid URL.')
            return

        self.start_button.setEnabled(False)
        self.perform_verification_until_200(1)  # Changed to 1 minute for testing purposes
        self.start_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
