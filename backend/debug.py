import cv2
import time 
import requests
import json
import os
import sys, time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

app = QApplication(sys.argv)
window = QWidget()
palette = window.palette()
window.setWindowTitle('Keep Going')
palette.setColor(QPalette.Window, QColor('white'))
window.setPalette(palette)
window.setGeometry(100, 100, 500, 300)

label = QLabel('KEEP GOING')
label.setFont(QFont('Tauri', 48, QFont.Bold))
label.setAlignment(Qt.AlignCenter)

layout = QVBoxLayout()
layout.addWidget(label)
window.setLayout(layout)
window.show()

def display_message(speedUp=False, slowDown=False):
    if speedUp:
        window.setWindowTitle('Speed Up')
        palette.setColor(QPalette.Window, QColor('green'))
        text = 'SPEED UP'
        label.setStyleSheet("color: white;")
    elif slowDown:
        window.setWindowTitle('Slow Down')
        palette.setColor(QPalette.Window, QColor('red'))
        text = 'SLOW DOWN'
        label.setStyleSheet("color: white;")
    else:
        window.setWindowTitle('Keep Going')
        palette.setColor(QPalette.Window, QColor('white'))
        text = 'KEEP GOING'
        label.setStyleSheet("color: black;")

    label.setText(text)
    window.setPalette(palette)

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

cap = cv2.VideoCapture(0)
time.sleep(1)
i = 0
i_changed = False
try: 
    while True: 
        ret, frame = cap.read() 

        if ret: 
            cv2.imshow('Frame', frame) 

            
            cv2.imwrite(f'frame-{i}.jpg', frame)



            params = {
                "img_path" : f"/Users/andre/Projects/competition/build-for-good/backend/frame-{i}.jpg",
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
                    if(maxemotion == attentiveness):
                        attentive_count += 1
                    if(maxemotion == confusion):
                        confused_count += 1
                print(f"attentive: {attentive_count}\nbored: {bored_count}\nconfused: {confused_count}")



                if(bored_count >= attentive_count and bored_count >= confused_count):
                    display_message(speedUp=True)
                elif(confused_count >= attentive_count and confused_count >= bored_count):
                    display_message(slowDown=True)
                else:
                    display_message()

            except Exception as e:
                print("people not found!")
                print(f"\n\n\n ERROR: {e} \n\n\n")
                pass
            
            i+=5
            time.sleep(5)
            
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break 
        else:  
            break 
finally:  
    cap.release() 
    cv2.destroyAllWindows() 
