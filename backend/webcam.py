import sys
import cv2
import time
import requests
import json
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class Student:
    def __init__(self, neutral, sadness, surprise, happiness, anger, fear):
        self.neutral = neutral
        self.sadness = sadness
        self.surprise = surprise
        self.happiness = happiness
        self.anger = anger
        self.fear = fear

    def calculate_boredom(self):
        boredom_score = (0.035 * self.neutral) + (1.24e-06 * self.sadness) + (0.00113 * self.surprise) + (0.941 * self.happiness) + (3.88e-05 * self.anger) + (1.28e-05 * self.fear)
        return(boredom_score)

    def calculate_attentiveness(self):
        attentiveness_score = (0.79 * self.neutral) + (0.000638 * self.sadness) + (0.000275 * self.surprise) + (0.000638 * self.happiness) + (0.184 * self.anger) + (0.002 * self.fear)
        return attentiveness_score

    def calculate_confusion(self):
        confusion_score = (0.042 * self.neutral) + (0.042 * self.sadness) + (0.019 * self.surprise) + (0.001 * self.happiness) + (0.002 * self.anger) + (0.898 * self.fear)
        return confusion_score
    

    def print_scores(self):
        print("Emotion Scores:")
        print(f"Neutral: {self.neutral}")
        print(f"Sadness: {self.sadness}")
        print(f"Surprise: {self.surprise}")
        print(f"Happiness: {self.happiness}")
        print(f"Anger: {self.anger}")
        print(f"Fear: {self.fear}")


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
                    
                    self.change_pixmap_signal.emit(True, False)

                    params = {
                        "img_path" : f"/Users/andre/Projects/competition/build-for-good/backend/frame.jpg",
                        "actions" : ["emotion"]
                    }


                    x = requests.post("http://127.0.0.1:5000/analyze", json=params)

                    x_dict = json.loads(x.text)


                    student_dict = []

                    try:
                        for j,person in enumerate(x_dict['results']):
                            student_dict.append(
                                Student(
                                    person['emotion']['neutral'],
                                    person['emotion']['sad'],
                                    person['emotion']['surprise'],
                                    person['emotion']['happy'],
                                    person['emotion']['angry'],
                                    person['emotion']['fear']
                                ))
                            
                        attentive_count = 0
                        bored_count = 0
                        confused_count = 0
                        for student in student_dict:
                            boredom = student.calculate_boredom()
                            attentiveness = student.calculate_attentiveness()
                            confusion = student.calculate_confusion()
                            maxemotion = max([boredom,attentiveness,confusion])
                            if(maxemotion == boredom):
                                bored_count += 1
                                print(f"bored: {boredom}")
                            if(maxemotion == attentiveness):
                                attentive_count += 1
                                f"attentiveness: {attentiveness}"
                            if(maxemotion == confusion):
                                confused_count += 1
                                f"confusion: {confusion}"
                        print(f"attentive: {attentive_count}\nbored: {bored_count}\nconfused: {confused_count}")



                        if(bored_count >= attentive_count and bored_count >= confused_count):
                            self.change_pixmap_signal.emit(True, False)
                        elif(confused_count >= attentive_count and confused_count >= bored_count):
                            self.change_pixmap_signal.emit(False, True)
                        else:
                            self.change_pixmap_signal.emit(False, False)

                    except Exception as e:
                        print("people not found!")
                        print(f"\n\n\n ERROR: {e} \n\n\n")
                        pass

                    os.remove(f'/Users/andre/Projects/competition/build-for-good/backend/frame.jpg')
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
