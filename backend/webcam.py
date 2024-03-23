import sys
import cv2
import time
import requests
import json
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(bool, bool)

    def run(self):
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        try:
            while True:
                ret, frame = cap.read()
                if ret:
                    # Process frame...
                    cv2.imwrite('frame.jpg', frame)
                    # Simulate analysis result for demonstration
                    self.change_pixmap_signal.emit(True, False)
                    time.sleep(5)
        finally:
            cap.release()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Analysis Window')
        self.setGeometry(100, 100, 500, 300)
        self.label = QLabel('KEEP GOING', self)
        self.label.setFont(QFont('Tauri', 48, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.updateUI(False, False)

    def updateUI(self, speedUp, slowDown):
        if speedUp:
            self.setWindowTitle('Speed Up')
            self.palette().setColor(QPalette.Window, QColor('green'))
            self.label.setText('SPEED UP')
            self.label.setStyleSheet("color: white;")
        elif slowDown:
            self.setWindowTitle('Slow Down')
            self.palette().setColor(QPalette.Window, QColor('red'))
            self.label.setText('SLOW DOWN')
            self.label.setStyleSheet("color: white;")
        else:
            self.setWindowTitle('Keep Going')
            self.palette().setColor(QPalette.Window, QColor('white'))
            self.label.setText('KEEP GOING')
            self.label.setStyleSheet("color: black;")
        self.setPalette(self.palette())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    thread = VideoThread()
    thread.change_pixmap_signal.connect(mainWindow.updateUI)
    thread.start()
    mainWindow.show()
    sys.exit(app.exec_())
